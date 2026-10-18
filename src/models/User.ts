import mongoose, { Schema } from "mongoose";

const UserModel = new Schema({
  name: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true,
  },
  password: {
    type: String,
    select: false,
  },
  passwordHash: {
    type: String,
    required: true,
  },
});

const User = mongoose.models.User || mongoose.model("User", UserModel);
export default User;
