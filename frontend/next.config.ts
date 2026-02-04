import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Strict mode for React to catch potential issues
  reactStrictMode: true,

  // Environment variables exposed to the browser
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    NEXT_PUBLIC_BETTER_AUTH_URL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:3000',
  },

  // Disable x-powered-by header for security
  poweredByHeader: false,

  // Production optimization
  compress: true,
};

export default nextConfig;
