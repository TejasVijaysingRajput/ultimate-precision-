import mongoose from "mongoose";

let connectionPromise: Promise<typeof mongoose> | null = null;

const dbConfig = async () => {
  if (mongoose.connection.readyState === 1) {
    return mongoose;
  }

  if (connectionPromise) {
    return connectionPromise;
  }

  const uri = process.env.MONGO_URI;
  if (!uri) {
    throw new Error("MONGO_URI is not configured");
  }

  connectionPromise = mongoose.connect(uri).catch((error) => {
    connectionPromise = null;
    throw error;
  });

  return connectionPromise;
};

export default dbConfig;
