from typing import List
from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl



# MESSAGE


class Message(BaseModel):

    role: Literal[
        "user",
        "assistant"
    ]

    content: str = Field(
        ...,
        min_length=1,
        max_length=4000
    )



# CHAT REQUEST


class ChatRequest(BaseModel):

    messages: List[Message] = Field(
        ...,
        min_length=1,
        max_length=20
    )



# RECOMMENDATION


class Recommendation(BaseModel):

    name: str

    url: HttpUrl

    test_type: str



# CHAT RESPONSE


class ChatResponse(BaseModel):

    reply: str

    recommendations: List[
        Recommendation
    ] = Field(
        default_factory=list,
        max_length=10
    )

    end_of_conversation: bool

