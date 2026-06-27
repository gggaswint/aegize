import type { Metadata } from "next";
import { Hanken_Grotesk, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const sans = Hanken_Grotesk({
  subsets: ["latin"],
  variable: "--font-hanken",
  display: "swap",
});

const mono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jbmono",
  display: "swap",
});

const description =
  "Aegize is the runtime layer between autonomous AI agents and the tools they use — identity, policy, permissions, approvals, audit logging, observability, and runtime governance for every AI action.";

export const metadata: Metadata = {
  metadataBase: new URL("https://aegize.com"),
  title: {
    default: "Aegize — Infrastructure for autonomous AI agents",
    template: "%s — Aegize",
  },
  description,
  keywords: [
    "AI agents",
    "runtime governance",
    "agent infrastructure",
    "policy",
    "permissions",
    "audit",
    "autonomous AI",
  ],
  authors: [{ name: "Aegize" }],
  openGraph: {
    type: "website",
    url: "https://aegize.com",
    title: "Aegize — Infrastructure for autonomous AI agents",
    description,
    siteName: "Aegize",
    images: [{ url: "/og.png", width: 1920, height: 1080, alt: "Aegize" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Aegize — Infrastructure for autonomous AI agents",
    description,
    images: ["/og.png"],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`no-js ${sans.variable} ${mono.variable}`}
      suppressHydrationWarning
    >
      <body className="font-sans antialiased">
        {/* Mark JS as available before paint so scroll-reveal content is hidden
            only when we can actually animate it in. No JS -> content stays visible. */}
        <script
          dangerouslySetInnerHTML={{
            __html:
              "document.documentElement.classList.remove('no-js');document.documentElement.classList.add('js');",
          }}
        />
        <div className="bg-atmosphere" aria-hidden="true" />
        <a
          href="#main"
          className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-md focus:bg-surface focus:px-4 focus:py-2 focus:text-sm focus:text-fg"
        >
          Skip to content
        </a>
        {children}
      </body>
    </html>
  );
}
