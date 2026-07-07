import React, { useMemo, useState, useEffect } from "react";
import {
  Box,
  Flex,
  Icon,
  Text,
  VStack,
  Collapse,
  Image,
  useColorModeValue,
} from "@chakra-ui/react";
import { FaChevronDown, FaChevronUp } from "react-icons/fa";
import { useNavigate, useLocation } from "react-router-dom";
import { getSidebarByRole } from "../../config/navigation";
import useAuth from "../../hooks/useAuth";
import DefaultLogo from "../../assets/pharmacy-icons/pharmacy-logo.svg";
import layout from "../../styles/common/layout";
import typography from "../../styles/common/typography";
import icons from "../../styles/common/icons";
import { colors, shadows } from "../../styles/common/colors";
import transitions from "../../styles/common/transitions";

const hasActiveChild = (menu, pathname) => {
  if (!menu.children) return false;

  return menu.children.some(
    (child) =>
      child.path === pathname ||
      (child.children && hasActiveChild(child, pathname)),
  );
};

const isMenuActive = (menu, pathname) => {
  return (
    menu.path === pathname || (menu.children && hasActiveChild(menu, pathname))
  );
};

const getDefaultOpenMenus = (menus, pathname) => {
  let opened = [];

  menus.forEach((menu) => {
    if (menu.children) {
      if (hasActiveChild(menu, pathname)) {
        opened.push(menu.id);
      }

      opened = [...opened, ...getDefaultOpenMenus(menu.children, pathname)];
    }
  });

  return opened;
};

const MenuItem = ({
  item,
  level,
  pathname,
  navigate,
  openedMenus,
  setOpenedMenus,
}) => {
  const hasChildren = item.children?.length > 0;

  const isOpen = openedMenus.includes(item.id);

  const isActive = isMenuActive(item, pathname);

  const textColor = useColorModeValue(colors.textPrimary, colors.white);

  const toggleMenu = () => {
    if (!hasChildren) return;

    if (isOpen) {
      setOpenedMenus([]);
    } else {
      setOpenedMenus([item.id]);
    }
  };

  return (
    <Box>
      <Flex
        sx={layout.sidebarItem}
        className={isActive ? "sidebar-item active" : "sidebar-item"}
        pl={`${level * 20 + 14}px`}
        color={isActive ? colors.white : textColor}
        borderRadius="10px"
        transition={transitions.normal}
        cursor="pointer"
        _hover={{
          bg: isActive ? colors.primary : colors.backgroundSecondary,
        }}
        onClick={() => {
          if (hasChildren) {
            toggleMenu();
          } else {
            navigate(item.path);
          }
        }}
      >
        <Flex sx={layout.sidebarItemContent}>
          {item.icon && (
            <Icon
              as={item.icon}
              {...icons.sidebarIcon}
              color={isActive ? colors.white : colors.primary}
            />
          )}

          <Text
            {...typography.sidebarLabel}
            color={isActive ? colors.white : colors.textPrimary}
            letterSpacing=".2px"
          >
            {item.label}
          </Text>
        </Flex>

        {hasChildren && (
          <Icon
            as={isOpen ? FaChevronUp : FaChevronDown}
            sx={layout.sidebarChevron}
            color={isActive ? colors.white : colors.textSecondary}
            transform={isOpen ? "rotate(180deg)" : "rotate(0deg)"}
          />
        )}
      </Flex>

      {hasChildren && (
        <Collapse in={isOpen} animateOpacity>
          <VStack align="stretch" spacing={1} sx={layout.sidebarSubMenu}>
            {item.children.map((child, index) => (
              <MenuItem
                key={child.id ?? child.path ?? `${item.id}-${index}`}
                item={child}
                level={level + 1}
                pathname={pathname}
                navigate={navigate}
                openedMenus={openedMenus}
                setOpenedMenus={setOpenedMenus}
              />
            ))}
          </VStack>
        </Collapse>
      )}
    </Box>
  );
};

/* ===================================================
   SIDEBAR COMPONENT
=================================================== */

const Sidebar = () => {
  const { role, user } = useAuth();

  const navigate = useNavigate();
  const { pathname } = useLocation();

  const sidebarMenus = useMemo(() => {
    if (!role) return [];
    return getSidebarByRole(role);
  }, [role]);

  const defaultOpened = useMemo(
    () => getDefaultOpenMenus(sidebarMenus, pathname),
    [sidebarMenus, pathname],
  );

  const [openedMenus, setOpenedMenus] = useState(defaultOpened);

  useEffect(() => {
    setOpenedMenus(defaultOpened);
  }, [defaultOpened]);

  const logoSrc =
    user?.company_logo || user?.logo || user?.organization?.logo || DefaultLogo;

  return (
    <Box
      sx={{
        ...layout.sidebarContainer,
        position: "sticky",
        top: 0,
        overflow: "hidden",
      }}
    >
      {/* =========================
          HEADER
      ========================= */}

      <Flex
        sx={{
          ...layout.sidebarHeader,
          minH: "80px",
        }}
      >
        <Box
          display="flex"
          justifyContent="center"
          alignItems="center"
          w="100%"
        >
          <Image
            src={logoSrc}
            alt="Company Logo"
            fallbackSrc={DefaultLogo}
            maxH="56px"
            maxW="170px"
            objectFit="contain"
          />
        </Box>
      </Flex>

      {/* =========================
          MENU
      ========================= */}

      <Box
        sx={{
          ...layout.sidebarContent,
          px: 3,
        }}
      >
        <VStack align="stretch" spacing={2}>
          {sidebarMenus.map((menu, index) => (
            <MenuItem
              key={menu.id ?? menu.path ?? `menu-${index}`}
              item={menu}
              level={0}
              pathname={pathname}
              navigate={navigate}
              openedMenus={openedMenus}
              setOpenedMenus={setOpenedMenus}
            />
          ))}
        </VStack>
      </Box>
    </Box>
  );
};

export default Sidebar;
