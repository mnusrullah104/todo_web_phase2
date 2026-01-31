/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // Use Turbopack (default in Next.js 16)
  turbopack: {
    // Empty config to silence the warning
  },

  // Optimize CSS
  experimental: {
    optimizeCss: true,
  },
};

module.exports = nextConfig;
