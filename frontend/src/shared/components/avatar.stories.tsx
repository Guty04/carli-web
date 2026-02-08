import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { Avatar } from "./avatar";

const meta = {
  title: "shared/Avatar",
  component: Avatar,
  argTypes: {
    name: { control: "text" },
    size: { control: { type: "range", min: 24, max: 64, step: 4 } },
  },
} satisfies Meta<typeof Avatar>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: { name: "John Doe", size: 40 },
};

export const SingleName: Story = {
  args: { name: "Admin", size: 40 },
};

export const NoName: Story = {
  args: { name: "", size: 40 },
};

export const Small: Story = {
  args: { name: "Jane Smith", size: 32 },
};

export const Large: Story = {
  args: { name: "Jane Smith", size: 48 },
};

export const AllSizes: Story = {
  render: () => (
    <div className="flex items-end gap-(--space-4)">
      <Avatar name="User" size={24} />
      <Avatar name="User" size={32} />
      <Avatar name="User" size={40} />
      <Avatar name="User" size={48} />
      <Avatar name="User" size={64} />
    </div>
  ),
};
