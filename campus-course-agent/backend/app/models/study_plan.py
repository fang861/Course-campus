from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from app.database import Base


class StudyPlan(Base):
    __tablename__ = "study_plan"
    __table_args__ = {
        UniqueConstraint("user_id", "turn_id", name="up_study_plan_user_turn"),
        {"comment": "学习计划"},
    }

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), comment="课程名词", nullable=False
    )
    content: Mapped[str] = mapped_column(Text, comment="计划内容", nullable=False)
    turn_id: Mapped[str | None] = mapped_column(
        String(32), comment="MCP对话轮次ID", nullable=True
    )
