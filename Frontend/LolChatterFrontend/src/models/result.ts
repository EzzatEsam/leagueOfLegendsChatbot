export interface Result<T> {
    success: boolean;
    data: T | null;
    message: string | null;
  }