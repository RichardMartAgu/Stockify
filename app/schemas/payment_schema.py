from pydantic import BaseModel, Field


class CheckoutSessionResponse(BaseModel):
    sessionId: str = Field(examples=['cs_test_a1xIsb7VFA4HITehZmT8BtIHDWJiALzdFTA81zAgWPkvr2YHQu6l'])