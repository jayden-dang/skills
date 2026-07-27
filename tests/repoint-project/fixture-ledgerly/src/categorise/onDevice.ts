import { loadModel } from "./model";

// ARCH-4: categorisation is on-device. Transaction text must never leave.
// The bundled model is 41 MB and ships inside the app binary.
const model = loadModel("categoriser-v3.tflite");

export function categorise(merchantRaw: string, amountMinor: number): string {
  const features = tokenise(merchantRaw.toLowerCase());
  return model.predict(features, amountMinor).topLabel;
}
