"use client";

import { useSession } from "@clerk/nextjs";
import { Button } from "@workspace/ui/components/shadcn/button";
import {
	Dialog,
	DialogContent,
	DialogDescription,
	DialogHeader,
	DialogTitle,
	DialogTrigger,
} from "@workspace/ui/components/shadcn/dialog";
import { Input } from "@workspace/ui/components/shadcn/input";
import { Label } from "@workspace/ui/components/shadcn/label";
import { Check, Copy, Key, Loader2 } from "lucide-react";
import { useState } from "react";

export function CreateTokenButton() {
	const { session, isLoaded } = useSession();
	const [token, setToken] = useState<string>("");
	const [isLoading, setIsLoading] = useState(false);
	const [isOpen, setIsOpen] = useState(false);
	const [hasCopied, setHasCopied] = useState(false);
	const [error, setError] = useState<string | null>(null);

	if (
		!isLoaded ||
		!session?.user ||
		session.user.publicMetadata.role !== "developer"
	) {
		return null;
	}

	const generateToken = async () => {
		if (!session) return;

		setIsLoading(true);
		setError(null);
		try {
			const newToken = await session.getToken({ template: "lifetime_token" });
			if (newToken) {
				setToken(newToken);
			} else {
				setError("Failed to generate token");
			}
		} catch (error) {
			console.error("Error generating token:", error);
			setError("Error generating token");
		} finally {
			setIsLoading(false);
		}
	};

	const copyToClipboard = async () => {
		if (!token) return;
		await navigator.clipboard.writeText(token);
		setHasCopied(true);
		setTimeout(() => setHasCopied(false), 2000);
	};

	const handleOpenChange = (open: boolean) => {
		setIsOpen(open);
		if (!open) {
			// Reset state when closing
			setToken("");
			setHasCopied(false);
			setError(null);
		}
	};

	return (
		<Dialog open={isOpen} onOpenChange={handleOpenChange}>
			<DialogTrigger asChild>
				<Button variant="outline" size="sm" className="gap-2">
					<Key className="h-4 w-4" />
					Create API Token
				</Button>
			</DialogTrigger>
			<DialogContent className="sm:max-w-md">
				<DialogHeader>
					<DialogTitle>Create Long-Lived API Token</DialogTitle>
					<DialogDescription>
						Generate a permanent authentication token for external use. Treat
						this token like a password.
					</DialogDescription>
				</DialogHeader>
				<div className="flex flex-col gap-4 py-4">
					{!token ? (
						<div className="flex flex-col items-center justify-center gap-4 py-8">
							<Button onClick={generateToken} disabled={isLoading}>
								{isLoading ? (
									<>
										<Loader2 className="mr-2 h-4 w-4 animate-spin" />
										Generating...
									</>
								) : (
									"Generate Token"
								)}
							</Button>
							{error && <p className="text-sm text-destructive">{error}</p>}
						</div>
					) : (
						<div className="flex flex-col gap-2">
							<Label htmlFor="token">Your API Token</Label>
							<div className="flex items-center gap-2">
								<Input
									id="token"
									value={token}
									readOnly
									className="font-mono text-xs"
								/>
								<Button
									size="icon"
									variant="outline"
									onClick={copyToClipboard}
									className="shrink-0"
								>
									{hasCopied ? (
										<Check className="h-4 w-4" />
									) : (
										<Copy className="h-4 w-4" />
									)}
								</Button>
							</div>
							<div className="flex justify-between items-center mt-2">
								<p className="text-xs text-muted-foreground">
									Make sure to copy this token now.
								</p>
								{hasCopied && (
									<span className="text-xs text-green-500 font-medium animate-in fade-in slide-in-from-bottom-1">
										Copied to clipboard!
									</span>
								)}
							</div>
						</div>
					)}
				</div>
			</DialogContent>
		</Dialog>
	);
}
