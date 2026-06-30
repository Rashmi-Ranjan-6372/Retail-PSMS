import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { verifyOTP, resendOTP } from "../../api/authAPI";
import useAuth from "../../hooks/useAuth";

const VerifyOTP = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { login } = useAuth();

    const user_id = location.state?.user_id;
    const username = location.state?.username;

    const [otp, setOtp] = useState("");
    const [loading, setLoading] = useState(false);
    const [resending, setResending] = useState(false);
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");

    useEffect(() => {
        if (!user_id) {
            navigate("/login");
        }
    }, [user_id, navigate]);

    const handleVerify = async (e) => {
        e.preventDefault();

        setError("");
        setMessage("");

        if (otp.length !== 6) {
            setError("Please enter a valid 6-digit OTP.");
            return;
        }

        try {
            setLoading(true);

            const res = await verifyOTP({
                user_id,
                otp,
            });

            if (res.data.success) {
                login({
                    user: res.data.user,
                    tokens: {
                        access: res.data.access,
                        refresh: res.data.refresh,
                    },
                });

                navigate("/dashboard", { replace: true });
                return;
            }

            setError(res.data.message || "Invalid OTP.");
        } catch (err) {
            setError(
                err.response?.data?.message ||
                "OTP verification failed."
            );
        } finally {
            setLoading(false);
        }
    };

    const handleResend = async () => {
        try {
            setResending(true);
            setError("");
            setMessage("");

            const res = await resendOTP({
                user_id,
            });

            if (res.data.success) {
                setMessage("A new OTP has been sent to your registered email.");
            } else {
                setError(res.data.message);
            }
        } catch (err) {
            setError(
                err.response?.data?.message ||
                "Unable to resend OTP."
            );
        } finally {
            setResending(false);
        }
    };

    return (
        <div style={styles.container}>
            <div style={styles.card}>
                <h2 style={styles.title}>Email Verification</h2>

                <p style={styles.subtitle}>
                    Enter the 6-digit OTP sent to your registered email.
                </p>

                {username && (
                    <p style={styles.user}>
                        Username: <strong>{username}</strong>
                    </p>
                )}

                {error && <div style={styles.error}>{error}</div>}
                {message && <div style={styles.success}>{message}</div>}

                <form onSubmit={handleVerify}>
                    <input
                        type="text"
                        value={otp}
                        maxLength={6}
                        placeholder="Enter OTP"
                        onChange={(e) =>
                            setOtp(e.target.value.replace(/\D/g, ""))
                        }
                        style={styles.input}
                    />

                    <button
                        type="submit"
                        style={styles.button}
                        disabled={loading}
                    >
                        {loading ? "Verifying..." : "Verify OTP"}
                    </button>
                </form>

                <button
                    type="button"
                    onClick={handleResend}
                    style={styles.resendButton}
                    disabled={resending}
                >
                    {resending ? "Sending..." : "Resend OTP"}
                </button>

                <button
                    type="button"
                    style={styles.backButton}
                    onClick={() => navigate("/login")}
                >
                    Back to Login
                </button>
            </div>
        </div>
    );
};

export default VerifyOTP;

const styles = {
    container: {
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "linear-gradient(135deg,#F8FAFC,#EEF6FF)",
        padding: "20px",
        fontFamily: "Inter, Arial",
    },

    card: {
        width: "100%",
        maxWidth: "420px",
        background: "#fff",
        padding: "30px",
        borderRadius: "16px",
        boxShadow: "0 10px 25px rgba(0,0,0,.08)",
    },

    title: {
        textAlign: "center",
        marginBottom: "10px",
        color: "#1E293B",
    },

    subtitle: {
        textAlign: "center",
        color: "#64748B",
        marginBottom: "20px",
    },

    user: {
        textAlign: "center",
        marginBottom: "20px",
        color: "#334155",
    },

    input: {
        width: "100%",
        height: "50px",
        borderRadius: "8px",
        border: "1px solid #CBD5E1",
        fontSize: "22px",
        letterSpacing: "10px",
        textAlign: "center",
        outline: "none",
        boxSizing: "border-box",
        marginBottom: "20px",
    },

    button: {
        width: "100%",
        padding: "12px",
        border: "none",
        borderRadius: "8px",
        background: "#2563EB",
        color: "#fff",
        fontWeight: "600",
        cursor: "pointer",
        marginBottom: "15px",
    },

    resendButton: {
        width: "100%",
        padding: "12px",
        border: "1px solid #2563EB",
        background: "#fff",
        color: "#2563EB",
        borderRadius: "8px",
        cursor: "pointer",
        marginBottom: "10px",
    },

    backButton: {
        width: "100%",
        padding: "12px",
        border: "none",
        background: "#E2E8F0",
        borderRadius: "8px",
        cursor: "pointer",
    },

    error: {
        background: "#FEE2E2",
        color: "#DC2626",
        padding: "10px",
        borderRadius: "8px",
        marginBottom: "15px",
        textAlign: "center",
    },

    success: {
        background: "#DCFCE7",
        color: "#15803D",
        padding: "10px",
        borderRadius: "8px",
        marginBottom: "15px",
        textAlign: "center",
    },
};