import "./globals.css";

export const metadata = {
  title: "Plano Mensal",
  description: "Automação de preenchimento do Plano Mensal",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
