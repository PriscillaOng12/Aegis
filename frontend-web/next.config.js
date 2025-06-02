/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    appDir: true,
  },
  env: {
    API_BASE: process.env.API_BASE || 'http://localhost:8000',
  },
};

module.exports = nextConfig;