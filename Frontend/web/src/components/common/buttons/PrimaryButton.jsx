import { Button } from "@chakra-ui/react";
import { primaryButton } from "../../../styles/components/buttons";

const PrimaryButton = ({
  children,
  isLoading,
  loadingText,
  leftIcon,
  rightIcon,
  ...props
}) => {
  return (
    <Button
      sx={primaryButton}
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

export default PrimaryButton;
