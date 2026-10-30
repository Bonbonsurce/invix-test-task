import type { NextConfig } from "next";

const apiTarget = process.env.API_REWRITE_TARGET ?? "http://127.0.0.1:8000";
const minioTarget = process.env.MINIO_REWRITE_TARGET ?? "http://127.0.0.1:9000";

const nextConfig: NextConfig = {
  output: "standalone",
  images: {
    remotePatterns: [
      { protocol: "http", hostname: "localhost", port: "9000", pathname: "/**" },
      { protocol: "https", hostname: "**" },
    ],
  },
  async rewrites() {
    return [
      { source: "/api/:path*", destination: `${apiTarget}/api/:path*` },
      { source: "/s3/:path*", destination: `${minioTarget}/:path*` },
    ];
  },
};

export default nextConfig;
