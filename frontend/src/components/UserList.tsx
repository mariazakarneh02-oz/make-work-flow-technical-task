import type { User } from "../types/user";

interface UserListProps {
  users: User[];
  onEdit: (user: User) => void;
  onDelete: (id: number) => void;
}

export function UserList({
  users,
  onEdit,
  onDelete,
}: UserListProps) {
  if (users.length === 0) {
    return <p>No users found.</p>;
  }

  return (
    <div className="user-list">
      {users.map((user) => (
        <div className="user-card" key={user.id}>
          <div>
            <h3>{user.name}</h3>
            <p>{user.email}</p>
          </div>

          <div className="actions">
            <button onClick={() => onEdit(user)}>
              Edit
            </button>

            <button onClick={() => onDelete(user.id)}>
              Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}