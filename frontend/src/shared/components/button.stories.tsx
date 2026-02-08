import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { ArrowRight, Check, Pencil, Plus, X } from "lucide-react";
import { Button } from "./button";

const meta = {
  title: "shared/Button",
  component: Button,
  argTypes: {
    variant: {
      control: "select",
      options: [
        "primary-dark",
        "primary-accent",
        "secondary",
        "ghost-success",
        "ghost-danger",
        "ghost-text",
      ],
    },
    loading: { control: "boolean" },
    disabled: { control: "boolean" },
    iconPosition: { control: "select", options: ["left", "right"] },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const PrimaryDark: Story = {
  args: { children: "Create Project", variant: "primary-dark" },
};

export const PrimaryAccent: Story = {
  args: { children: "Confirm", variant: "primary-accent" },
};

export const Secondary: Story = {
  args: { children: "Edit", variant: "secondary" },
};

export const GhostSuccess: Story = {
  args: { children: "Approve", variant: "ghost-success" },
};

export const GhostDanger: Story = {
  args: { children: "Reject", variant: "ghost-danger" },
};

export const GhostText: Story = {
  args: { children: "Cancel", variant: "ghost-text" },
};

export const WithIconLeft: Story = {
  args: {
    children: "New Project",
    variant: "primary-dark",
    icon: <Plus size={20} />,
    iconPosition: "left",
  },
};

export const WithIconRight: Story = {
  args: {
    children: "Continue",
    variant: "primary-accent",
    icon: <ArrowRight size={20} />,
    iconPosition: "right",
  },
};

export const Loading: Story = {
  args: { children: "Creating...", variant: "primary-dark", loading: true },
};

export const Disabled: Story = {
  args: { children: "Submit", variant: "primary-dark", disabled: true },
};

export const AllVariants: Story = {
  render: () => (
    <div className="flex flex-col gap-(--space-4)">
      <Button variant="primary-dark" icon={<Plus size={20} />}>
        Primary Dark
      </Button>
      <Button
        variant="primary-accent"
        icon={<Check size={20} />}
        iconPosition="right"
      >
        Primary Accent
      </Button>
      <Button variant="secondary" icon={<Pencil size={16} />}>
        Secondary
      </Button>
      <Button variant="ghost-success" icon={<Check size={16} />}>
        Approve
      </Button>
      <Button variant="ghost-danger" icon={<X size={16} />}>
        Reject
      </Button>
      <Button variant="ghost-text">Cancel</Button>
      <Button variant="primary-dark" loading>
        Loading
      </Button>
      <Button variant="primary-dark" disabled>
        Disabled
      </Button>
    </div>
  ),
};
