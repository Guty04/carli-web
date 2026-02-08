import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { CategoryBadge, StatusBadge } from "./badge";

const statusMeta = {
  title: "shared/StatusBadge",
  component: StatusBadge,
  argTypes: {
    variant: {
      control: "select",
      options: ["success", "error", "warning", "info", "neutral"],
    },
    dot: { control: "boolean" },
  },
} satisfies Meta<typeof StatusBadge>;

export default statusMeta;
type Story = StoryObj<typeof statusMeta>;

export const Success: Story = {
  args: { variant: "success", children: "Passed" },
};

export const Error: Story = {
  args: { variant: "error", children: "Failed" },
};

export const Warning: Story = {
  args: { variant: "warning", children: "Warning" },
};

export const Info: Story = {
  args: { variant: "info", children: "In Progress" },
};

export const Neutral: Story = {
  args: { variant: "neutral", children: "Unknown" },
};

export const WithoutDot: Story = {
  args: { variant: "success", children: "Passed", dot: false },
};

export const AllVariants: Story = {
  args: { variant: "success", children: "All Variants" },
  render: () => (
    <div className="flex flex-wrap gap-(--space-3)">
      <StatusBadge variant="success">Passed</StatusBadge>
      <StatusBadge variant="error">Failed</StatusBadge>
      <StatusBadge variant="warning">Pending</StatusBadge>
      <StatusBadge variant="info">In Progress</StatusBadge>
      <StatusBadge variant="neutral">Unknown</StatusBadge>
    </div>
  ),
};

export const CategoryBadgeStory: Story = {
  name: "Category Badge",
  args: { variant: "neutral", children: "Category" },
  render: () => (
    <div className="flex flex-wrap gap-(--space-3)">
      <CategoryBadge>BACKEND</CategoryBadge>
      <CategoryBadge>FRONTEND</CategoryBadge>
    </div>
  ),
};
