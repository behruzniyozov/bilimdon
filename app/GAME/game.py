from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db,Session
from sqlalchemy.orm import Session
from app.models import *
from GAME.schemas import *
from app.main import get_current_user


router = APIRouter(prefix="/game", tags=["Game"])


@router.get("/read-games", response_model=List[ReadGame])
async def read_games(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    
    games = db.query(Game).all()
    if not games:
        raise HTTPException(status_code=404, detail="No games found")
    return games

@router.get("/read-games", response_model=ReadGame)
async def get_games(
    user: ReadGame,
    db: Session = Depends(get_db)):
    
    games = db.query(Game).filter(Game.id==user.id).all()
    if not games:
        raise HTTPException(status_code=404, detail="No games found")
    return games

@router.post("/create-games", response_model=CreateGame)    
async def create_games(
    game_data: CreateGame,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="You are not allowed to create a game")

    db_game = Game(
        owner=game_data.owner,
        title=game_data.title,
        description=game_data.description,
        topic=game_data.topic,
        score=game_data.score,
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(minutes=game_data.end_time), 
    )

    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


@router.patch("/update-games/{game_id}", response_model=UpdateGame) 
async def update_game(
    game_data: UpdateGame,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_game = db.query(Game).filter(Game.id == game_data.id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")

    if db_game.owner != current_user.username and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="You are not allowed to update this game")

    db_game.topic = game_data.topic
    db_game.score = game_data.score
    db_game.start_time = game_data.start_time
    db_game.end_time = game_data.end_time

    db.commit()
    db.refresh(db_game)
    return db_game

@router.delete("/delete-games/{game_id}")
async def delete_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_game = db.query(Game).filter(Game.id == game_id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")

    if db_game.owner != current_user.username and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this game")

    db.delete(db_game)
    db.commit()
    return "Game deleted successfully"