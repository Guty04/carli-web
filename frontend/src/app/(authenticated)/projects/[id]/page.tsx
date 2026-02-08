import { ProjectOverviewContent } from "@/features/main/components/project-overview-content";

export default async function ProjectOverviewPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <ProjectOverviewContent projectId={id} />;
}
