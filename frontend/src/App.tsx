import { useState } from "react";

import {
  createUser,
  deleteUser,
  fetchUsers,
  updateUser,
} from "./api/users";
import { UserList } from "./components/UserList";
import type { User } from "./types/user";

function App() {
  const [users, setUsers] = useState<User[]>([]);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [editingUser, setEditingUser] = useState<User | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFetchUsers = async () => {
    try {
      setLoading(true);
      setError(null);

      const data = await fetchUsers();
      setUsers(data);
    } catch {
      setError("Failed to fetch users");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setError(null);

      if (editingUser) {
        const updatedUser = await updateUser(
          editingUser.id,
          name,
          email,
        );

        setUsers((currentUsers) =>
          currentUsers.map((user) =>
            user.id === updatedUser.id
              ? updatedUser
              : user,
          ),
        );

        setEditingUser(null);
      } else {
        const newUser = await createUser(name, email);

        setUsers((currentUsers) => [
          ...currentUsers,
          newUser,
        ]);
      }

      setName("");
      setEmail("");
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (user: User) => {
    setEditingUser(user);
    setName(user.name);
    setEmail(user.email);
  };

  const handleDelete = async (id: number) => {
    try {
      setLoading(true);
      setError(null);

      await deleteUser(id);

      setUsers((currentUsers) =>
        currentUsers.filter((user) => user.id !== id),
      );
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="page">
      <section className="container">
        <div className="header">
          <h1>Users</h1>
          <p>Manage application users</p>
        </div>

        <div className="form">
          <input
            type="text"
            placeholder="Name"
            value={name}
            onChange={(event) =>
              setName(event.target.value)
            }
          />

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(event) =>
              setEmail(event.target.value)
            }
          />

          <button
            onClick={handleSubmit}
            disabled={loading}
          >
            {editingUser ? "Update User" : "Add User"}
          </button>
        </div>

        <button
          className="fetch-button"
          onClick={handleFetchUsers}
          disabled={loading}
        >
          {loading ? "Loading..." : "Fetch Users"}
        </button>

        {error && <p className="error">{error}</p>}

        <UserList
          users={users}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      </section>
    </main>
  );
}

export default App;