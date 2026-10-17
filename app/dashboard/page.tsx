import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const { userId } = await auth();

  if (!userId) {
    redirect("/");
  }

  return (
    <div>
      <h1 className="text-3xl font-bold">Dashboard</h1>
    </div>
  );
}

