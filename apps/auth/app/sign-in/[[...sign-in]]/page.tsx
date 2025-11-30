import { SignIn } from "@clerk/nextjs";
import { AuthCard } from "../../components/auth-card";

export default async function Page({
	searchParams,
}: {
	searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
	const { redirect_url } = await searchParams;
	const finalRedirectUrl =
		typeof redirect_url === "string" ? redirect_url : undefined;

	return (
		<AuthCard>
			<SignIn forceRedirectUrl={finalRedirectUrl} />
		</AuthCard>
	);
}
