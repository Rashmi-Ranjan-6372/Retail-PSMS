import {
  Box,
  VStack,
  Text,
  Collapse,
  Flex,
  Icon,
} from "@chakra-ui/react";

import {
  FaTachometerAlt,
  FaBoxes,
  FaCapsules,
  FaIndustry,
  FaTruck,
  FaUserFriends,
  FaDollarSign,
  FaWarehouse,
  FaUndo,
  FaClock,
  FaMoneyCheckAlt,
  FaFileInvoice,
  FaFileInvoiceDollar,
  FaBook,
  FaUserTie,
  FaCog,
  FaCalendarCheck,
  FaMapMarkedAlt,
  FaChevronDown,
  FaChevronUp,
} from "react-icons/fa";

import { FaChartColumn } from "react-icons/fa6";

import { useNavigate, useLocation } from "react-router-dom";
import { useState } from "react";

const sidebarStructure = [

  {
    label: "Dashboard",
    icon: FaTachometerAlt,
    path: "/dashboard",
  },

  {
    label: "Masters",
    icon: FaBoxes,

    items: [
      {
        label: "Products",
        icon: FaCapsules,
        path: "/masters/products",
      },

      {
        label: "Categories",
        icon: FaBoxes,
        path: "/masters/categories",
      },

      {
        label: "Manufacturers",
        icon: FaIndustry,
        path: "/masters/manufacturers",
      },

      {
        label: "Suppliers",
        icon: FaTruck,
        path: "/masters/suppliers",
      },

      {
        label: "Customers",
        icon: FaUserFriends,
        path: "/masters/customers",
      },

      {
        label: "Sales Offers",
        icon: FaDollarSign,
        path: "/masters/sales-offers",
      },
    ],
  },

  {
    label: "Inventory",
    icon: FaWarehouse,

    items: [
      {
        label: "Stock Transactions",
        icon: FaBoxes,
        path: "/inventory/stock-transactions",
      },

      {
        label: "Stock Batches",
        icon: FaBoxes,
        path: "/inventory/stock-batches",
      },

      {
        label: "Stock Adjustments",
        icon: FaUndo,
        path: "/inventory/stock-adjustments",
      },

      {
        label: "Stock Transfers",
        icon: FaUndo,
        path: "/inventory/stock-transfers",
      },

      {
        label: "Expiry Damages",
        icon: FaClock,
        path: "/inventory/expiry-damages",
      },
    ],
  },

  {
    label: "Purchases",
    icon: FaTruck,

    items: [
      {
        label: "Purchases",
        icon: FaFileInvoice,
        path: "/purchases",
      },

      {
        label: "Purchase Returns",
        icon: FaUndo,
        path: "/purchase-returns",
      },

      {
        label: "Payments",
        icon: FaMoneyCheckAlt,
        path: "/payments",
      },
    ],
  },

  {
    label: "Sales",
    icon: FaDollarSign,

    items: [
      {
        label: "Sales",
        icon: FaFileInvoiceDollar,
        path: "/sales",
      },

      {
        label: "Sales Returns",
        icon: FaUndo,
        path: "/sales-returns",
      },

      {
        label: "Receipts",
        icon: FaMoneyCheckAlt,
        path: "/receipts",
      },
    ],
  },

  {
    label: "Reports",
    icon: FaChartColumn,

    items: [
      {
        label: "Sales Report",
        icon: FaFileInvoice,
        path: "/reports/sales",
      },

      {
        label: "Purchase Report",
        icon: FaTruck,
        path: "/reports/purchases",
      },

      {
        label: "Stock Report",
        icon: FaWarehouse,
        path: "/reports/stock",
      },

      {
        label: "Profit & Loss",
        icon: FaDollarSign,
        path: "/reports/profit-loss",
      },

      {
        label: "Expiry Report",
        icon: FaClock,
        path: "/reports/expiry",
      },

      {
        label: "Low Stock Report",
        icon: FaBoxes,
        path: "/reports/low-stock",
      },

      {
        label: "Customer Ledger",
        icon: FaUserFriends,
        path: "/reports/customer-ledger",
      },

      {
        label: "Supplier Ledger",
        icon: FaUserTie,
        path: "/reports/supplier-ledger",
      },

      {
        label: "Product Ledger",
        icon: FaBook,
        path: "/reports/product-ledger",
      },
    ],
  },

  {
    label: "Branch Management",
    icon: FaMapMarkedAlt,

    items: [
      {
        label: "Branches",
        icon: FaMapMarkedAlt,
        path: "/branches",
      },
    ],
  },

  {
    label: "User Management",
    icon: FaUserFriends,

    items: [
      {
        label: "Users",
        icon: FaUserFriends,
        path: "/users",
      },

      {
        label: "User Sessions",
        icon: FaClock,
        path: "/users/sessions",
      },

      {
        label: "Login Logs",
        icon: FaClock,
        path: "/users/login-logs",
      },

      {
        label: "Audit Logs",
        icon: FaBook,
        path: "/users/audit-logs",
      },
    ],
  },

  {
    label: "Settings",
    icon: FaCog,

    items: [
      {
        label: "General Settings",
        icon: FaCog,
        path: "/settings/general",
      },

      {
        label: "Financial Years",
        icon: FaCalendarCheck,
        path: "/settings/financial-years",
      },
    ],
  },

  {
    label: "Account",
    icon: FaUserTie,

    items: [
      {
        label: "Profile",
        icon: FaUserTie,
        path: "/account/profile",
      },

      {
        label: "Change Password",
        icon: FaCog,
        path: "/account/change-password",
      },

      {
        label: "Logout",
        icon: FaUndo,
        path: "/logout",
      },
    ],
  },
];

const Sidebar = () => {

  const navigate = useNavigate();
  const location = useLocation();

  const [openMenu, setOpenMenu] = useState(null);

  const toggleMenu = (label) => {
    setOpenMenu(openMenu === label ? null : label);
  };

  return (
    <Box
      w="260px"
      h="100vh"
      bg="gray.800"
      color="white"
      p={4}
      overflowY="auto"
    >

      <Text
        fontSize="2xl"
        mb={6}
        fontWeight="bold"
      >
        Pharmacy ERP
      </Text>

      <VStack align="stretch" spacing={2}>

        {sidebarStructure.map((menu, index) => {

          const isOpen = openMenu === menu.label;

          if (menu.items) {

            return (
              <Box key={index}>

                <Flex
                  align="center"
                  justify="space-between"
                  p={2}
                  cursor="pointer"
                  borderRadius="md"
                  _hover={{ bg: "gray.700" }}
                  onClick={() => toggleMenu(menu.label)}
                >

                  <Flex align="center" gap={3}>
                    <Icon as={menu.icon} />
                    <Text>{menu.label}</Text>
                  </Flex>

                  <Icon
                    as={isOpen ? FaChevronUp : FaChevronDown}
                  />

                </Flex>

                <Collapse in={isOpen}>
                  <VStack
                    align="stretch"
                    pl={6}
                    mt={2}
                    spacing={1}
                  >

                    {menu.items.map((subMenu, subIndex) => (

                      <Flex
                        key={subIndex}
                        align="center"
                        gap={3}
                        p={2}
                        cursor="pointer"
                        borderRadius="md"
                        bg={
                          location.pathname === subMenu.path
                            ? "green.600"
                            : "transparent"
                        }
                        _hover={{ bg: "gray.700" }}
                        onClick={() => navigate(subMenu.path)}
                      >

                        <Icon as={subMenu.icon} />
                        <Text fontSize="sm">
                          {subMenu.label}
                        </Text>

                      </Flex>

                    ))}

                  </VStack>
                </Collapse>

              </Box>
            );
          }

          return (
            <Flex
              key={index}
              align="center"
              gap={3}
              p={2}
              cursor="pointer"
              borderRadius="md"
              bg={
                location.pathname === menu.path
                  ? "green.600"
                  : "transparent"
              }
              _hover={{ bg: "gray.700" }}
              onClick={() => navigate(menu.path)}
            >

              <Icon as={menu.icon} />
              <Text>{menu.label}</Text>

            </Flex>
          );
        })}

      </VStack>

    </Box>
  );
};

export default Sidebar;