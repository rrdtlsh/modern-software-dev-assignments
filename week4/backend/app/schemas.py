from pydantic import BaseModel


class NoteCreate(BaseModel):
    """Payload schema used when creating a new note."""

    title: str
    content: str


class NoteRead(BaseModel):
    """Representation of a note returned from the API."""

    id: int
    title: str
    content: str

    class Config:
        from_attributes = True


class ActionItemCreate(BaseModel):
    """Payload schema used when creating a new action item."""

    description: str


class ActionItemRead(BaseModel):
    """Representation of an action item returned from the API."""

    id: int
    description: str
    completed: bool

    class Config:
        from_attributes = True
