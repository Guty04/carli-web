import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { Card } from "./card";

const meta = {
  title: "shared/Card",
  component: Card,
  argTypes: {
    hoverable: { control: "boolean" },
  },
} satisfies Meta<typeof Card>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: (
      <div className="flex flex-col gap-(--space-2)">
        <h3 className="text-(--text-subheading) font-semibold">Card Title</h3>
        <p className="text-(--color-neutral-500)">
          This is a basic card with some content inside.
        </p>
      </div>
    ),
  },
};

export const Hoverable: Story = {
  args: {
    hoverable: true,
    children: (
      <div className="flex flex-col gap-(--space-2)">
        <h3 className="text-(--text-subheading) font-semibold">
          Hoverable Card
        </h3>
        <p className="text-(--color-neutral-500)">
          Hover over this card to see the lift effect.
        </p>
      </div>
    ),
  },
};
