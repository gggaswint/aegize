import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Fully static site -> export to ./out for zero-config hosting (Cloudflare Pages, etc.)
  output: "export",
  // Emit directory-style routes (/playground/index.html) so they serve on any
  // static host, not just ones that do clean-URL rewrites.
  trailingSlash: true,
  images: { unoptimized: true },
  reactStrictMode: true,
};

export default nextConfig;
