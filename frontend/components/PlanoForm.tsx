"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";

type FormData = {
  componente: string;
  nomeArquivo: string;
  professor: string;
  ano: string;
  turma: string;
  periodo: string;
  objetivos: string;
  habilidades: string;
  objetosConhecimento: string;
  metodologia: string;
  recursos: string;
  avaliacoes: string;
  referencias: string;
  assinaturaProfessor: string;
};

const initialValues: FormData = {
  componente: "",
  nomeArquivo: "",
  professor: "",
  ano: "",
  turma: "",
  periodo: "",
  objetivos: "",
  habilidades: "",
  objetosConhecimento: "",
  metodologia: "",
  recursos: "",
  avaliacoes: "",
  referencias: "",
  assinaturaProfessor: "",
};

function Field({
  label,
  register,
  name,
  placeholder,
  textarea = false,
  required = false,
}: {
  label: string;
  register: any;
  name: keyof FormData;
  placeholder?: string;
  textarea?: boolean;
  required?: boolean;
}) {
  const common =
    "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm outline-none transition focus:border-slate-600 focus:ring-2 focus:ring-slate-200";

  return (
    <label className="block">
      <span className="mb-2 block text-sm font-semibold text-slate-700">
        {label} {required && <span className="text-red-500">*</span>}
      </span>
      {textarea ? (
        <textarea
          {...register(name, required ? { required: "Campo obrigatório" } : {})}
          rows={5}
          placeholder={placeholder}
          className={common + " resize-y"}
        />
      ) : (
        <input
          {...register(name, required ? { required: "Campo obrigatório" } : {})}
          placeholder={placeholder}
          className={common}
        />
      )}
    </label>
  );
}

export default function PlanoForm() {
  const { register, handleSubmit, reset } = useForm<FormData>({
    defaultValues: initialValues,
  });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function onSubmit(data: FormData) {
    setIsSubmitting(true);
    setMessage("");
    setError("");

    try {
      const response = await fetch("/api/planos", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Não foi possível gerar o documento.");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      const disposition = response.headers.get("content-disposition") ?? "";
      const encodedFilename = disposition.match(/filename\*=UTF-8''([^;]+)/i)?.[1];
      const quotedFilename = disposition.match(/filename="([^"]+)"/i)?.[1];
      link.href = url;
      link.download = encodedFilename
        ? decodeURIComponent(encodedFilename)
        : quotedFilename ?? `${data.nomeArquivo.trim()}.docx`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      setMessage("Documento gerado com sucesso. O arquivo foi baixado automaticamente.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro inesperado ao gerar o documento.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-bold">1. Identificação</h2>
        <p className="mt-1 mb-6 text-sm text-slate-500">
          Informações básicas do plano.
        </p>

        <div className="grid gap-5 md:grid-cols-2">
          <Field label="Componente" register={register} name="componente" required placeholder="Ex.: Matemática" />
          <div>
            <Field
              label="Nome do arquivo (sem extensão)"
              register={register}
              name="nomeArquivo"
              required
              placeholder="Ex.: Plano mensal de língua portuguesa"
            />
            <p className="mt-2 text-sm text-slate-500">
              A extensão .docx será adicionada automaticamente.
            </p>
          </div>
          <Field label="Professor" register={register} name="professor" required placeholder="Nome completo" />
          <Field label="Ano" register={register} name="ano" required placeholder="Ex.: 6º Ano" />
          <Field label="Turma" register={register} name="turma" required placeholder="Ex.: 601" />
          <Field label="Período" register={register} name="periodo" required placeholder="Ex.: Agosto de 2026" />
        </div>
      </section>

      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-bold">2. Planejamento</h2>
        <p className="mt-1 mb-6 text-sm text-slate-500">
          Conteúdo que será inserido nas áreas correspondentes do documento oficial.
        </p>

        <div className="space-y-5">
          <Field label="Objetivos" register={register} name="objetivos" textarea required />
          <Field label="Habilidades" register={register} name="habilidades" textarea required />
          <Field label="Objetos do conhecimento" register={register} name="objetosConhecimento" textarea required />
          <Field label="Metodologia / Estratégias Didáticas" register={register} name="metodologia" textarea required />
          <Field label="Recursos Didáticos" register={register} name="recursos" textarea required />
          <Field label="Avaliações" register={register} name="avaliacoes" textarea required />
          <Field label="Referências" register={register} name="referencias" textarea />
        </div>
      </section>

      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-bold">4. Finalização</h2>
        <p className="mt-1 mb-6 text-sm text-slate-500">
          Informação usada no campo de assinatura do modelo.
        </p>

        <Field
          label="Assinatura Professor(a)"
          register={register}
          name="assinaturaProfessor"
          placeholder="Nome do professor(a)"
        />
      </section>

      {message && (
        <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-800">
          {message}
        </div>
      )}

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800">
          {error}
        </div>
      )}

      <div className="flex flex-col gap-3 sm:flex-row sm:justify-end">
        <button
          type="button"
          onClick={() => {
            reset(initialValues);
            setMessage("");
            setError("");
          }}
          className="rounded-xl border border-slate-300 bg-white px-6 py-3 text-sm font-semibold hover:bg-slate-50"
        >
          Limpar
        </button>
        <button
          type="submit"
          disabled={isSubmitting}
          className="rounded-xl bg-slate-900 px-6 py-3 text-sm font-semibold text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-70"
        >
          {isSubmitting ? "Gerando..." : "Gerar documento"}
        </button>
      </div>
    </form>
  );
}
