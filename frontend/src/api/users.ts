import type { User } from "../types/user";

const API_URL = "http://localhost:8000";

function getErrorMessage(error: unknown): string {
  if (
    typeof error === "object" &&
    error !== null &&
    "detail" in error
  ) {
    const detail = (
      error as {
        detail: unknown;
      }
    ).detail;

    if (typeof detail === "string") {
      return detail;
    }

    if (Array.isArray(detail)) {
      return detail
        .map((item) => {
          if (
            typeof item === "object" &&
            item !== null &&
            "msg" in item
          ) {
            return String(item.msg);
          }

          return "Validation error";
        })
        .join(", ");
    }
  }

  return "Something went wrong";
}

export async function fetchUsers(): Promise<User[]> {
  const response = await fetch(`${API_URL}/users`);

  if (!response.ok) {
    throw new Error("Failed to fetch users");
  }

  return response.json();
}

export async function createUser(
  name: string,
  email: string,
): Promise<User> {
  const response = await fetch(`${API_URL}/users`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name,
      email,
    }),
  });

  if (!response.ok) {
    const error = await response.json();

    throw new Error(getErrorMessage(error));
  }

  return response.json();
}

export async function updateUser(
  id: number,
  name: string,
  email: string,
): Promise<User> {
  const response = await fetch(`${API_URL}/users/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name,
      email,
    }),
  });

  if (!response.ok) {
    const error = await response.json();

    throw new Error(getErrorMessage(error));
  }

  return response.json();
}

export async function deleteUser(
  id: number,
): Promise<void> {
  const response = await fetch(`${API_URL}/users/${id}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    const error = await response.json();

    throw new Error(getErrorMessage(error));
  }
}