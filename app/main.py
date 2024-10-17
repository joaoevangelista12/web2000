from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .database import get_db
from .models import Montadora
from .schemas import MontadoraCreate, MontadoraUpdate

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Página principal (listar montadoras)
@app.get("/", response_class=HTMLResponse)
async def read_montadoras(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Montadora))
    montadoras = result.scalars().all()
    return templates.TemplateResponse("index.html", {"request": request, "montadoras": montadoras})

# Página de criação de montadora (GET)
@app.get("/create", response_class=HTMLResponse)
async def create_montadora_form(request: Request):
    return templates.TemplateResponse("create_montadora.html", {"request": request})

# Criar nova montadora (POST)
@app.post("/create")
async def create_montadora(nome: str = Form(...), pais: str = Form(...), ano_fundacao: int = Form(...), db: AsyncSession = Depends(get_db)):
    montadora = Montadora(nome=nome, pais=pais, ano_fundacao=ano_fundacao)
    db.add(montadora)
    await db.commit()
    return templates.TemplateResponse("create_montadora.html", {"request": request, "message": "Montadora adicionada com sucesso!"})

# Página de edição de montadora (GET)
@app.get("/edit/{montadora_id}", response_class=HTMLResponse)
async def edit_montadora_form(montadora_id: str, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Montadora).filter(Montadora.id == montadora_id))
    montadora = result.scalars().first()
    if not montadora:
        raise HTTPException(status_code=404, detail="Montadora não encontrada")
    return templates.TemplateResponse("edit_montadora.html", {"request": request, "montadora": montadora})

# Atualizar montadora (POST)
@app.post("/edit/{montadora_id}")
async def update_montadora(montadora_id: str, nome: str = Form(...), pais: str = Form(...), ano_fundacao: int = Form(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Montadora).filter(Montadora.id == montadora_id))
    montadora = result.scalars().first()
    if not montadora:
        raise HTTPException(status_code=404, detail="Montadora não encontrada")
    montadora.nome = nome
    montadora.pais = pais
    montadora.ano_fundacao = ano_fundacao
    await db.commit()
    return templates.TemplateResponse("edit_montadora.html", {"request": request, "montadora": montadora, "message": "Montadora atualizada com sucesso!"})

# Excluir montadora
@app.get("/delete/{montadora_id}")
async def delete_montadora(montadora_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Montadora).filter(Montadora.id == montadora_id))
    montadora = result.scalars().first()
    if not montadora:
        raise HTTPException(status_code=404, detail="Montadora não encontrada")
    await db.delete(montadora)
    await db.commit()
    return {"message": "Montadora excluída com sucesso"}
