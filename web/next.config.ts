import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Fully static site -> export to ./out for zero-config hosting (Cloudflare Pages, etc.)
  output: "export",
  images: { unoptimized: true },
  reactStrictMode: true,
};

export default nextConfig;
