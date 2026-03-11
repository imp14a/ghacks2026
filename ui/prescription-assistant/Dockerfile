
# Dockerfile

# Stage 1: Build the Next.js application
FROM node:24-slim AS builder

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build the application
RUN npm run build

# Stage 2: Create the production image
FROM node:24-slim AS runner

# Set working directory
WORKDIR /app

# Copy the built application from the builder stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json

# Install production dependencies
RUN npm install --production

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["npm", "start"]
