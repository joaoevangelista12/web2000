from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from .models import Montadora

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Página principal (listar montadoras)
@app.get("/", response_class=HTMLResponse)
async def read_montadoras(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Montadora))
    montadoras = result.scalars().all()
    return templates.TemplateResponse("index.html", {"request": request, "montadoras": montadoras})

# Página de criação de montadora
@app.get("/create", response_class=HTMLResponse)
async def create_montadora_form(request: Request):
    return templates.TemplateResponse("create_montadora.html", {"request": request})

@app.post("/create")
async def create_montadora(nome: str = Form(...), pais: str = Form(...), ano_fundacao: int = Form(...), db: AsyncSession = Depends(get_db)):
    montadora = Montadora(nome=nome, pais=pais, ano_fundacao=ano_fundacao)
    db.add(montadora)
    await db.commit()
    return templates.TemplateResponse("create_montadora.html", {"request": request, "message": "Montadora adicionada com sucesso!"})
