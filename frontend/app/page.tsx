import PlanoForm from "../components/PlanoForm";

export default function Home() {
  return (
    <main className="min-h-screen px-4 py-8 md:px-8">
      <div className="mx-auto max-w-5xl">
        <header className="mb-8">
          <p className="mb-2 text-sm font-semibold uppercase tracking-wider text-slate-500">
            Automação de documentos
          </p>
          <h1 className="text-3xl font-bold tracking-tight md:text-4xl">
            Plano Mensal
          </h1>
          <p className="mt-2 max-w-2xl text-slate-600">
            Preencha as informações abaixo. O documento oficial será usado
            como modelo e somente os campos editáveis serão preenchidos.
          </p>
        </header>

        <PlanoForm />
      </div>
    </main>
  );
}
