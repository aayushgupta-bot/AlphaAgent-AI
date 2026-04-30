// Import global styles for the entire application
import "./globals.css";

// Metadata configuration for SEO and browser tab information
export const metadata = {
  title: "AlphaAgent AI — Intelligent Stock Analysis",
  description:
    "Agent-driven stock analysis, prediction, and explanation powered by ML and LLM.",
};

// Root layout component that wraps all pages in the app
export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-screen">{children}</body>
    </html>
  );
}
