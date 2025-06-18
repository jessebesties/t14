import pathway as pw
from pathway.xpacks.llm import llms
import json

class StockLLMAnalyzer:
    def __init__(self, model_name="microsoft/DialoGPT-small"):
        self.model = llms.HFPipelineChat(model=model_name)
    
    def create_analysis_prompt(self, ticker, price_data, news_data):
        """Create a prompt for stock analysis"""
        
        prompt = f"""
You are a financial advisor. Analyze the following data for {ticker} and provide a simple recommendation.

PRICE DATA:
- Current Price: ${price_data.get('current_price', 0):.2f}
- Price Change: {price_data.get('price_change_pct', 0):.2f}%
- Volume: {price_data.get('volume', 0):,}
- 5-day High: ${price_data.get('high_5d', 0):.2f}
- 5-day Low: ${price_data.get('low_5d', 0):.2f}

NEWS SUMMARY:
{news_data}

Based on this information, should someone BUY, SELL, or HOLD {ticker}? 
Explain your reasoning in simple terms that anyone can understand.
Keep your response under 200 words and structure it as:

RECOMMENDATION: [BUY/SELL/HOLD]
REASONING: [Your explanation in simple language]
CONFIDENCE: [High/Medium/Low]
"""
        return prompt
    
    def analyze_stock_data(self, combined_data):
        """Analyze combined stock data using LLM"""
        
        # Group data by ticker
        grouped = combined_data.groupby(pw.this.ticker).reduce(
            ticker=pw.this.ticker,
            latest_price=pw.reducers.latest(pw.this.current_price),
            price_change_pct=pw.reducers.latest(pw.this.price_change_pct),
            volume=pw.reducers.latest(pw.this.volume),
            high_5d=pw.reducers.latest(pw.this.high_5d),
            low_5d=pw.reducers.latest(pw.this.low_5d),
            news_summary=pw.reducers.tuple(pw.this.title)  # Collect news titles
        )
        
        # Create analysis prompts
        analysis_prompts = grouped.select(
            ticker=pw.this.ticker,
            prompt=self.create_analysis_prompt(
                pw.this.ticker,
                {
                    'current_price': pw.this.latest_price,
                    'price_change_pct': pw.this.price_change_pct,
                    'volume': pw.this.volume,
                    'high_5d': pw.this.high_5d,
                    'low_5d': pw.this.low_5d
                },
                pw.this.news_summary
            )
        )
        
        # Generate LLM responses
        analysis_results = analysis_prompts.select(
            ticker=pw.this.ticker,
            analysis=self.model(pw.this.prompt)
        )
        
        return analysis_results
    
    def parse_analysis_response(self, response_text):
        """Parse the LLM response into structured data"""
        try:
            lines = response_text.strip().split('\n')
            
            recommendation = "HOLD"
            reasoning = "Analysis unavailable"
            confidence = "Low"
            
            for line in lines:
                if line.startswith("RECOMMENDATION:"):
                    recommendation = line.split(":", 1)[1].strip()
                elif line.startswith("REASONING:"):
                    reasoning = line.split(":", 1)[1].strip()
                elif line.startswith("CONFIDENCE:"):
                    confidence = line.split(":", 1)[1].strip()
            
            return {
                "recommendation": recommendation,
                "reasoning": reasoning,
                "confidence": confidence
            }
            
        except Exception as e:
            return {
                "recommendation": "HOLD",
                "reasoning": f"Error parsing analysis: {str(e)}",
                "confidence": "Low"
            }