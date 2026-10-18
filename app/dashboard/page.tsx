import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { getUserLinks } from "@/data/links";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { CreateLinkDialog } from "./create-link-dialog";
import { EditLinkDialog } from "./edit-link-dialog";
import { DeleteLinkDialog } from "./delete-link-dialog";

export default async function DashboardPage() {
  const { userId } = await auth();

  if (!userId) {
    redirect("/");
  }

  const links = await getUserLinks(userId);

  return (
    <div className="mx-auto w-full max-w-4xl space-y-6 p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <CreateLinkDialog />
      </div>

      {links.length === 0 ? (
        <Card>
          <CardHeader>
            <CardTitle>No links yet</CardTitle>
            <CardDescription>
              Create your first shortened link to get started.
            </CardDescription>
          </CardHeader>
        </Card>
      ) : (
        <ul className="space-y-4">
          {links.map((link) => (
            <li key={link.id}>
              <Card>
                <CardContent className="flex items-center justify-between gap-4">
                  <div className="min-w-0 space-y-1">
                    <a
                      href={`/l/${link.shortCode}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="font-medium hover:underline"
                    >
                      /l/{link.shortCode}
                    </a>
                    <p className="truncate text-sm text-muted-foreground">
                      {link.originalUrl}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      Created {link.createdAt.toLocaleDateString("en-US")}
                    </p>
                  </div>
                  <div className="flex shrink-0 items-center gap-2">
                    <EditLinkDialog link={link} />
                    <DeleteLinkDialog
                      linkId={link.id}
                      shortCode={link.shortCode}
                    />
                  </div>
                </CardContent>
              </Card>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

