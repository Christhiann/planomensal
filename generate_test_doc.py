from backend.app.main import generate_document_from_template, PlanoData

data = PlanoData(
    componente='Matemática',
    nomeArquivo='Plano mensal de matemática',
    professor='Alessandra',
    ano='8',
    turma='209',
    periodo='agosto de 2025',
    objetivos='Desenvolver o raciocínio lógico e a capacidade de resolução de problemas.',
    habilidades='Resolver problemas envolvendo operações matemáticas e interpretar informações.',
    objetosConhecimento='Números, operações e resolução de problemas.',
    metodologia='Aulas expositivas, resolução de exercícios e atividades práticas.',
    recursos='Quadro, livros didáticos e materiais de apoio.',
    avaliacoes='Avaliação contínua por meio de atividades e exercícios.',
    referencias='Livro didático adotado pela instituição.',
    assinaturaProfessor='Alessandra',
)

out = generate_document_from_template(data)
print('generated', out)
