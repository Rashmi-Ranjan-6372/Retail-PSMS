import { Button } from "@chakra-ui/react";
import { secondaryButton } from "../../../styles/components/buttons";

const SecondaryButton = ({
  children,
  isLoading,
  loadingText,
  leftIcon,
  rightIcon,
  ...props
}) => {
  return (
    <Button
      sx={secondaryButton}
      isLoading={isLoading}
      loadingText={loadingText}
      leftIcon={leftIcon}
      rightIcon={rightIcon}
      {...props}
    >
      {children}
    </Button>
  );
};

export default SecondaryButton;
