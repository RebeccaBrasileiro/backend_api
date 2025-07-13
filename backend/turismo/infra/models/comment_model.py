import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from turismo.domain.entities.comment import Comment
import uuid
from datetime import datetime
from turismo.infra.database import Base


class CommentModel(Base):
    __tablename__ = "comments"

    id: Mapped[str] = mapped_column(
        sa.String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    comment: Mapped[str] = mapped_column(sa.Text, nullable=False)

    # 🔴 Removida a foreign key para posts.id
    post_id: Mapped[str] = mapped_column(sa.String)  # Sem ForeignKey

    user_id: Mapped[str] = mapped_column(sa.String, sa.ForeignKey("users.id"))
    date: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.now())

    # 🔴 Removido relacionamento com PostModel
    # post = relationship("PostModel", back_populates="comments")

    user = relationship("UserModel", back_populates="comments")

    @classmethod
    def from_entity(cls, entity: Comment) -> "CommentModel":
        return cls(
            id=entity.id,
            comment=entity.comment,
            post_id=entity.post_id,
            user_id=entity.user_id,
            date=entity.date,
        )

    def to_entity(self) -> Comment:
        return Comment(
            id=self.id,
            comment=self.comment,
            post_id=self.post_id,
            user_id=self.user_id,
            date=self.date,
        )
