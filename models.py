from pydantic import BaseModel, Field
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from typing import Optional

class ProductInfo(BaseModel):
    product_name: str = Field(description="Official product name from manufacturer")
    details: str = Field(description="Key specifications and market positioning")
    tentative_price_usd: float = Field(description="Realistic market price in USD without symbols")

class ProductChatBot:
    def __init__(self):
        self.llm = OpenAI(
            model_name="gpt-3.5-turbo-instruct",
            temperature=0.3  
        )
        self.parser = PydanticOutputParser(pydantic_object=ProductInfo)
        
        self.prompt = PromptTemplate(
            template="""Act as an expert e-commerce price estimator. Analyze market prices for this product.
            Consider brand value, technical specifications, and competitor pricing.
            Provide a realistic USD price estimate without currency symbols.
            
            {format_instructions}
            
            Product to Estimate: {product_name}
            """,
            input_variables=["product_name"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions() + 
                "\nRespond with valid JSON. Price must be a positive number."
            }
        )
        
    def estimate_price(self, product_name: str) -> Optional[ProductInfo]:
        try:
            chain = self.prompt | self.llm | self.parser
            response = chain.invoke({"product_name": product_name})
            
            # Validate price range
            if not (10 <= response.tentative_price_usd <= 100000):  # Basic sanity check
                response.tentative_price_usd = 0.0
                
            return response
            
        except Exception as e:
            return ProductInfo(
                product_name="Estimation Error",
                details=str(e),
                tentative_price_usd=0.0
            )