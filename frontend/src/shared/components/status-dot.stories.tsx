import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { StatusDot } from "./status-dot";

const meta = {
  title: "shared/StatusDot",
  component: StatusDot,
  argTypes: {
    color: {
      control: "select",
      options: ["success", "error", "warning", "info", "neutral"],
    },
  },
} satisfies Meta<typeof StatusDot>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Success: Story = { args: { color: "success" } };
export const Error: Story = { args: { color: "error" } };
export const Warning: Story = { args: { color: "warning" } };
export const Info: Story = { args: { color: "info" } };
export const Neutral: Story = { args: { color: "neutral" } };

export const AllColors: Story = {
  render: () => (
    <div className="flex items-center gap-(--space-4)">
      {(["success", "error", "warning", "info", "neutral"] as const).map(
        (color) => (
          <div key={color} className="flex items-center gap-(--space-2)">
            <StatusDot color={color} />
            <span className=" capitalize">{color}</span>
          </div>
        ),
      )}
    </div>
  ),
  args: { color: "info" },
};
