"use client";
import { AnimatePresence, motion } from "framer-motion";
import { RadioGroup } from "@headlessui/react";
import { v4 as uuid } from "uuid";
import Link from "next/link";
import { useRef, useState, useEffect, useCallback, use } from "react";
import Webcam from "react-webcam";
import FileUpload from "@/components/uploader";
import { Textarea } from "@nextui-org/react";
import StepIndicator from "@/components/step";
import ReactPlayer from "react-player";
import Typewriter from "typewriter-effect";

import path from "path";

const maxstep = 9;
type DataFormat = {
	[key: string]: string[];
};
const CustomCheckbox = ({
	checked,
	onChange,
	label,
}: {
	checked: boolean;
	onChange: () => void;
	label: string;
}) => {
	return (
		<div
			className={`relative cursor-pointer rounded-lg border bg-white w-[400px]   px-6 py-4 shadow-sm focus:outline-none flex justify-between ${
				checked ? "border-blue-500 ring-2 ring-blue-200" : "border-gray-300"
			}`}
			onClick={onChange}
		>
			<span className="flex items-center">
				<span className="flex flex-col text-sm">
					<span className="font-medium text-gray-900">{label}</span>
				</span>
			</span>
			<span className="flex items-center ml-4">
				<input
					type="checkbox"
					checked={checked}
					onChange={onChange}
					className="form-checkbox h-5 w-5 text-blue-600 transition duration-150 ease-in-out"
				/>
			</span>
		</div>
	);
};
const interviewers = [
	{
		id: "1",
		name: "Female UK voice",
		description: "",
		sampleAudio: "/female_gb_sample.mp3",
	},
	{
		id: "2",
		name: "Female US voice",
		description: " ",
		sampleAudio: "/female_us_sample.mp3",
	},
	{
		id: "3",
		name: "Male UK voice",
		description: " ",
		sampleAudio: "/male_gb_sample.mp3",
	},
	{
		id: "4",
		name: "Male US voice",
		description: " ",
		sampleAudio: "/male_us_sample.mp3",
	},
];

const lengthOptions = [
	{
		id: "1min",
		name: "Quick Recap",
		description: "1 minute length",
	},
	{
		id: "2min",
		name: "Detailed",
		description: "2 minute length",
	},
	{
		id: "3min",
		name: "In-depth",
		description: "3 minute length",
	},
];

const styles = [
	{
		id: "1",
		name: "Formal",
		description: "A business-style script for meetings and presentations",
	},
	{
		id: "2",
		name: "Relaxed",
		description: "A casual script for daily use",
	},
	{
		id: "3",
		name: "Funny",
		description: "A funny script for friends and family",
	},
];

const music = [
	{
		id: "1",
		name: "Subtle",
		description: "Subtle white noise music",
		sampleAudio: "/subtle_sample.mp3",
	},
	{
		id: "2",
		name: "Energetic",
		description: "Lively background music",
		sampleAudio: "/energetic_sample.mp3",
	},
	{
		id: "3",
		name: "Formal",
		description: "News-like background music",
		sampleAudio: "/formal_sample.mp3",
	},
];

function classNames(...classes: string[]) {
	return classes.filter(Boolean).join(" ");
}
const gifUrls = [
	"https://giphy.com/gifs/film-cinema-david-lynch-M0l3KOk8KXOOk",
	"https://giphy.com/gifs/benglabs-movie-film-G0lXg7mTDf4MU",
	"https://giphy.com/gifs/film-editing-f-for-fake-Iyqv0kE4hUwYE",
	"https://giphy.com/gifs/BTTF-back-to-the-future-bttf-one-oziNormWuA6JrnbzY8",
	"https://giphy.com/gifs/asapnast-asap-nast-designer-boi-Ma0X1M9lQB4FruMaX3",
	"https://giphy.com/gifs/billy-wilder-sunset-boulevard-blvd-l6mBchxYZc7Sw",
];
export default function DemoPage() {
	const [selectedTopics, setSelectedTopics] = useState<string[]>([]);

	const [selectedMusic, setSelectedMusic] = useState(music[0]);
	const [selectedLength, setSelectedLength] = useState(lengthOptions[0]);
	const [selectedVoice, setSelectedVoice] = useState(interviewers[0]);
	const [selectedStyle, setSelectedStyle] = useState(styles[0]);
	const [step, setStep] = useState(1);
	const [serverIds, setServerIds] = useState<string[]>([]); // State to hold server IDs
	const [scriptValue, setScriptValue] = useState("");
	const [loadingScript, setLoadingScript] = useState(false);
	const [topics, setTopics] = useState<DataFormat>({});
	const [rawText, setRawText] = useState("");
	const [videoUrl, setVideoUrl] = useState("");
	const [videoError, setVideoError] = useState(false);
	const [videoLoading, setVideoLoading] = useState(true);
	const [scriptRefresh, setScriptRefresh] = useState(0);
	const [videoRefresh, setVideoRefresh] = useState(0);
	const [currentAudio, setCurrentAudio] = useState<HTMLAudioElement | null>(
		null
	);
	const [currentGifIndex, setCurrentGifIndex] = useState(0);

	const getEnv = async () => {
		try {
			const response = await fetch("/api/checkEnv", { method: "GET" });
			const data = await response.json();
			console.log("data", data);
			return data.isDocker;
		} catch (error) {
			console.error("Error checking environment:", error);
		}
	};

	console.log("env", getEnv());

	const deleteVideo = async () => {
		console.log("Deleting existing video");
		try {
			const response = await fetch("/api/deleteVideo", { method: "DELETE" });
			if (response.ok) {
				console.log("Existing video deleted");
			} else {
				console.error("Error deleting video:", response.statusText);
			}
		} catch (error) {
			console.error("Error deleting video:", error);
		}
	};
	const loadVideo = async () => {
		console.log("Loading video");
		const filePath = "/api/getVideo";

		try {
			setVideoLoading(true);
			const response = await fetch(filePath, { method: "GET" });

			if (response.ok) {
				const blob = await response.blob();
				const videoUrl = URL.createObjectURL(blob);
				setVideoUrl(videoUrl);
				setVideoLoading(false);
			} else {
				setTimeout(loadVideo, 10000);
			}
		} catch (error) {
			setVideoError(true);
		}
	};
	console.log("current step", step);
	useEffect(() => {
		deleteVideo(); // Delete the existing video on page load
	}, []);

	useEffect(() => {
		if (step === 8) {
			loadVideo(); // Start checking for a new video when step equals 7
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [step]);

	const handleServerId = (serverId: string) => {
		// Ensure the server ID is typed as a string
		setServerIds((currentServerIds) => [...currentServerIds, serverId]);
	};
	useEffect(() => {
		console.log("serverIds", serverIds);
		if (serverIds.length > 0) {
			const parsedData = JSON.parse(serverIds[0]);
			setRawText(parsedData.parsedText);

			const topicJson = JSON.parse(parsedData.topicjson);
			const mainTopics = Object.keys(topicJson);

			setTopics(topicJson);
			setSelectedTopics(mainTopics);

			console.log("topics", parsedData);
		}
	}, [serverIds]);
	const [lastScriptValues, setLastScriptValues] = useState<string[]>([]);

	useEffect(() => {
		async function fetchData() {
			if (step === 7) {
				setLoadingScript(true);
				console.log("selectedTopic", selectedTopics);
				console.log("selectedStyle", selectedStyle);
				console.log("selectedLength", selectedLength);
				try {
					const response = await fetch("/api/scriptGen", {
						method: "POST",
						headers: {
							"Content-Type": "application/json",
						},
						body: JSON.stringify({
							selectedTopics: selectedTopics,
							selectedStyle,
							selectedLength,
							selectedVoice,
							selectedMusic,
							nextresponse: true,
						}),
					});
					const data = await response.json();
					if (data.script !== "") {
						setLastScriptValues((prevValues) => [
							...prevValues,
							data.script,
						]);
					}
					setScriptValue(data.script);
					setLoadingScript(false);
				} catch (error) {
					// Handle the error here
				}
			}
		}
		fetchData();
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [step, scriptRefresh]);

	useEffect(() => {
		async function fetchData() {
			if (step === 8) {
				console.log("edited script", scriptValue);

				try {
					const response = await fetch("/api/videoGen", {
						method: "POST",
						headers: {
							"Content-Type": "application/json",
						},
						body: JSON.stringify({
							scriptValue,
							musicValue: selectedMusic,
						}),
					});
					// Process the data here
				} catch (error) {
					// Handle the error here
				}
			}
		}
		fetchData();
		if (currentAudio) {
			currentAudio.pause();

			currentAudio.currentTime = 0;
			setCurrentAudio(null);
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [step, videoRefresh]);

	return (
		<div className="flex flex-col md:flex-row h-screen">
			{" "}
			{/* Adjusted for full height */}
			<div className="  w-1/3 flex md:items-center justify-center p-4  ">
				{" "}
				{/* Added flex container styles */}
				<StepIndicator currentStep={step} />
			</div>
			<AnimatePresence>
				{step === maxstep ? (
					<div className="w-full min-h-screen flex flex-col px-4 pt-2 pb-8 md:px-8 md:py-2 bg-[#FCFCFC] relative overflow-x-hidden"></div>
				) : (
					<div className="flex md:flex-row w-full md:overflow-hidden">
						<div className="w-full w-5/6 flex flex-col items-center justify-center px-4 pt-2 pb-8  bg-gray-100">
							<motion.div
								initial={{ y: -10, opacity: 0 }}
								animate={{ y: 0, opacity: 1 }}
								transition={{
									duration: 1.25,
									ease: [0.23, 1, 0.32, 1],
								}}
								className="    flex   items-center justify-center bg-gray-100 z-10"
							>
								{step === 1 && (
									<h2 className="text-4xl font-bold text-[#1E2B3A] px-4 md:px-8 py-4">
										Upload a PDF report
									</h2>
								)}
								{step === 2 && (
									<h2 className="text-4xl font-bold text-[#1E2B3A] px-4 md:px-8 py-4">
										Choose video length
									</h2>
								)}
								{step === 3 && (
									<h2 className="text-4xl font-bold text-[#1E2B3A] px-4 md:px-8 py-4">
										Choose your voiceover speaker
									</h2>
								)}
								{step === 4 && (
									<h2 className="text-4xl font-bold text-[#1E2B3A] px-4 md:px-8 py-4">
										Choose your script style
									</h2>
								)}
								{step === 5 && (
									<h2 className="text-4xl font-bold text-[#1E2B3A] px-4 md:px-8 py-4">
										Choose your background music style
									</h2>
								)}
								{step === 6 && (
									<h2 className="text-4xl font-bold text-[#1E2B3A] px-4 md:px-8 py-4">
										Choose your topics
									</h2>
								)}
								{step === 7 && (
									<h2 className="text-4xl font-bold text-[#1E2B3A] px-4 md:px-8 py-4">
										Edit your script
									</h2>
								)}
								{step === 8 && (
									<h2 className="text-4xl font-bold text-[#1E2B3A] px-4 md:px-8 py-4">
										Video generation
									</h2>
								)}
							</motion.div>
							<div>
								{step === 1 ? (
									<motion.div
										initial={{ opacity: 0, y: 40 }}
										animate={{ opacity: 1, y: 0 }}
										exit={{ opacity: 0, y: -40 }}
										key="step-1"
										transition={{
											duration: 0.95,
											ease: [0.165, 0.84, 0.44, 1],
										}}
										className="max-w-lg mx-auto px-4 lg:px-0 flex flex-col items-center"
									>
										<p className="text-[14px]   text-[#1a2b3b] font-normal my-4">
											Select your files to be converted into a video
											report.{" "}
										</p>
										<div className="w-96">
											<FileUpload onServerId={handleServerId} />{" "}
											{/* Pass the callback to FileUpload */}
										</div>

										<div className="flex gap-[15px] justify-end mt-8">
											<div>
												<Link
													href="/"
													className="group rounded-full px-4 py-2 text-[13px] font-semibold transition-all flex items-center justify-center bg-[#f5f7f9] text-[#1E2B3A] no-underline active:scale-95 scale-100 duration-75"
													style={{
														boxShadow:
															"0 1px 1px #0c192714, 0 1px 3px #0c192724",
													}}
												>
													Back to home
												</Link>
											</div>
											<div>
												<button
													onClick={() => {
														setStep(step + 1);
													}}
													className="group rounded-full px-4 py-2 text-[13px] font-semibold transition-all flex items-center justify-center bg-[#1E2B3A] text-white hover:[linear-gradient(0deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.1)), #0D2247] no-underline flex gap-x-2  active:scale-95 scale-100 duration-75"
													style={{
														boxShadow:
															"0px 1px 4px rgba(13, 34, 71, 0.17), inset 0px 0px 0px 1px #061530, inset 0px 0px 0px 2px rgba(255, 255, 255, 0.1)",
													}}
												>
													<span> Continue </span>
													<svg
														className="w-5 h-5"
														viewBox="0 0 24 24"
														fill="none"
														xmlns="http://www.w3.org/2000/svg"
													>
														<path
															d="M13.75 6.75L19.25 12L13.75 17.25"
															stroke="#FFF"
															strokeWidth="1.5"
															strokeLinecap="round"
															strokeLinejoin="round"
														/>
														<path
															d="M19 12H4.75"
															stroke="#FFF"
															strokeWidth="1.5"
															strokeLinecap="round"
															strokeLinejoin="round"
														/>
													</svg>
												</button>
											</div>
										</div>
									</motion.div>
								) : step === 2 ? (
									<motion.div
										initial={{ opacity: 0, y: 40 }}
										animate={{ opacity: 1, y: 0 }}
										exit={{ opacity: 0, y: -40 }}
										key="step-2"
										transition={{
											duration: 0.95,
											ease: [0.165, 0.84, 0.44, 1],
										}}
										className=" mx-auto px-4 lg:px-0"
									>
										<div>
											<RadioGroup
												value={selectedLength}
												onChange={setSelectedLength}
											>
												<RadioGroup.Label className="sr-only">
													Server size
												</RadioGroup.Label>
												<div className="space-y-4 md:w-full">
													{lengthOptions.map((lengthOption) => (
														<RadioGroup.Option
															key={lengthOption.name}
															value={lengthOption}
															className={({ checked, active }) =>
																classNames(
																	checked
																		? "border-transparent"
																		: "border-gray-300",
																	active
																		? "border-blue-500 ring-2 ring-blue-200"
																		: "",
																	"relative cursor-pointer rounded-lg border bg-white w-[400px]   px-6 py-4 shadow-sm focus:outline-none w-[400px] justify-between"
																)
															}
														>
															{({ active, checked }) => (
																<>
																	<span className="flex items-center">
																		<span className="flex flex-col text-sm">
																			<RadioGroup.Label
																				as="span"
																				className="font-medium text-gray-900"
																			>
																				{lengthOption.name}
																			</RadioGroup.Label>
																			<RadioGroup.Description
																				as="span"
																				className="text-gray-500"
																			>
																				<span className="block">
																					{
																						lengthOption.description
																					}
																				</span>
																			</RadioGroup.Description>
																		</span>
																	</span>
																	<RadioGroup.Description
																		as="span"
																		className="flex text-sm ml-4 mt-0 flex-col text-right items-center justify-center"
																	>
																		<span className=" text-gray-500"></span>
																	</RadioGroup.Description>
																	<span
																		className={classNames(
																			active
																				? "border"
																				: "border-2",
																			checked
																				? "border-blue-500"
																				: "border-transparent",
																			"pointer-events-none absolute -inset-px rounded-lg"
																		)}
																		aria-hidden="true"
																	/>
																</>
															)}
														</RadioGroup.Option>
													))}
												</div>
											</RadioGroup>
										</div>
										<div className="flex gap-[15px] justify-end mt-8">
											<div>
												<button
													onClick={() => setStep(step - 1)}
													className="group rounded-full px-4 py-2 text-[13px] font-semibold transition-all flex items-center justify-center bg-[#f5f7f9] text-[#1E2B3A] no-underline active:scale-95 scale-100 duration-75"
													style={{
														boxShadow:
															"0 1px 1px #0c192714, 0 1px 3px #0c192724",
													}}
												>
													Previous step
												</button>
											</div>
											<div>
												<button
													onClick={() => {
														setStep(step + 1);
													}}
													className="group rounded-full px-4 py-2 text-[13px] font-semibold transition-all flex items-center justify-center bg-[#1E2B3A] text-white hover:[linear-gradient(0deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.1)), #0D2247] no-underline flex gap-x-2  active:scale-95 scale-100 duration-75"
													style={{
														boxShadow:
															"0px 1px 4px rgba(13, 34, 71, 0.17), inset 0px 0px 0px 1px #061530, inset 0px 0px 0px 2px rgba(255, 255, 255, 0.1)",
													}}
												>
													<span> Continue </span>
													<svg
														className="w-5 h-5"
														viewBox="0 0 24 24"
														fill="none"
														xmlns="http://www.w3.org/2000/svg"
													>
														<path
															d="M13.75 6.75L19.25 12L13.75 17.25"
															stroke="#FFF"
															strokeWidth="1.5"
															strokeLinecap="round"
															strokeLinejoin="round"
														/>
														<path
															d="M19 12H4.75"
															stroke="#FFF"
															strokeWidth="1.5"
															strokeLinecap="round"
															strokeLinejoin="round"
														/>
													</svg>
												</button>
											</div>
										</div>
									</motion.div>
								) : step === 3 ? (
									<motion.div
										initial={{ opacity: 0, y: 40 }}
										animate={{ opacity: 1, y: 0 }}
										exit={{ opacity: 0, y: -40 }}
										key="step-2"
										transition={{
											duration: 0.95,
											ease: [0.165, 0.84, 0.44, 1],
										}}
										className="max-w-lg mx-auto px-4 lg:px-0"
									>
										<div>
											<RadioGroup
												value={selectedVoice}
												onChange={setSelectedVoice}
											>
												<RadioGroup.Label className="sr-only">
													Server size
												</RadioGroup.Label>
												<div className="space-y-4">
													{interviewers.map((interviewer) => (
														<RadioGroup.Option
															key={interviewer.id}
															value={interviewer}
															className={({
																checked,
																active,
															}: {
																checked: boolean;
																active: boolean;
															}) =>
																classNames(
																	checked
																		? "border-transparent"
																		: "border-gray-300",
																	active
																		? "border-blue-500 ring-2 ring-blue-200"
																		: "",
																	"relative cursor-pointer rounded-lg border bg-white w-[400px]   px-6 py-4 shadow-sm focus:outline-none flex justify-between"
																)
															}
														>
															{({
																active,
																checked,
															}: {
																active: boolean;
																checked: boolean;
															}) => (
																<>
																	<span className="flex items-center">
																		<span className="flex flex-col text-sm">
																			<RadioGroup.Label
																				as="span"
																				className="font-medium text-gray-900"
																			>
																				{interviewer.name}
																			</RadioGroup.Label>
																			<RadioGroup.Description
																				as="span"
																				className="text-gray-500"
																			>
																				<span className="block">
																					{
																						interviewer.description
																					}
																				</span>
																			</RadioGroup.Description>
																		</span>
																	</span>
																	<RadioGroup.Description
																		as="span"
																		className="flex text-sm ml-4 mt-0 flex-col text-right items-center justify-center"
																	>
																		<span className="text-gray-500">
																			<button
																				onClick={() => {
																					if (
																						currentAudio
																					) {
																						currentAudio.pause();
																						currentAudio.currentTime = 0;
																					}
																					const audio =
																						new Audio(
																							interviewer.sampleAudio
																						);
																					audio.play();
																					setCurrentAudio(
																						audio
																					);
																				}}
																				className="group rounded-full px-3 py-1 text-[12px] font-semibold transition-all flex items-center justify-center bg-[#1E2B3A] text-white hover:bg-[#0D2247] no-underline active:scale-95 scale-100 duration-75"
																				style={{
																					boxShadow:
																						"0px 1px 4px rgba(13, 34, 71, 0.17), inset 0px 0px 0px 1px #061530, inset 0px 0px 0px 2px rgba(255, 255, 255, 0.1)",
																				}}
																			>
																				Play Sample
																			</button>
																		</span>
																	</RadioGroup.Description>
																	<span
																		className={classNames(
																			active
																				? "border"
																				: "border-2",
																			checked
																				? "border-blue-500"
																				: "border-transparent",
																			"pointer-events-none absolute -inset-px rounded-lg"
																		)}
																		aria-hidden="true"
																	/>
																</>
															)}
														</RadioGroup.Option>
													))}
												</div>
											</RadioGroup>
										</div>
										<div className="flex gap-[15px] justify-end mt-8">
											<div>
												<button
													onClick={() => setStep(step - 1)}
													className="group rounded-full px-4 py-2 text-[13px] font-semibold transition-all flex items-center justify-center bg-[#f5f7f9] text-[#1E2B3A] no-underline active:scale-95 scale-100 duration-75"
													style={{
														boxShadow:
															"0 1px 1px #0c192714, 0 1px 3px #0c192724",
													}}
												>
													Previous step
												</button>
											</div>
											<div>
												<button
													onClick={() => {
														setStep(step + 1);
													}}
													className="group rounded-full px-4 py-2 text-[13px] font-semibold transition-all flex items-center justify-center bg-[#1E2B3A] text-white hover:[linear-gradient(0deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.1)), #0D2247] no-underline flex gap-x-2  active:scale-95 scale-100 duration-75"
													style={{
														boxShadow:
															"0px 1px 4px rgba(13, 34, 71, 0.17), inset 0px 0px 0px 1px #061530, inset 0px 0px 0px 2px rgba(255, 255, 255, 0.1)",
													}}
												>
													<span> Continue </span>
													<svg
														className="w-5 h-5"
														viewBox="0 0 24 24"
														fill="none"
														xmlns="http://www.w3.org/2000/svg"
													>
														<path
															d="M13.75 6.75L19.25 12L13.75 17.25"
															stroke="#FFF"
															strokeWidth="1.5"
															strokeLinecap="round"
															strokeLinejoin="round"
														/>
														<path
															d="M19 12H4.75"
															stroke="#FFF"
															strokeWidth="1.5"
															strokeLinecap="round"
															strokeLinejoin="round"
														/>
													</svg>
												</button>
											</div>
										</div>
									</motion.div>
								) : step === 4 ? (
									<motion.div
										initial={{ opacity: 0, y: 40 }}
										animate={{ opacity: 1, y: 0 }}
										exit={{ opacity: 0, y: -40 }}
										key="step-2"
										transition={{
											duration: 0.95,
											ease: [0.165, 0.84, 0.44, 1],
										}}
										className="max-w-lg mx-auto px-4 lg:px-0"
									>
										<div>
											<RadioGroup
												value={selectedStyle}
												onChange={setSelectedStyle}
											>
												<RadioGroup.Label className="sr-only">
													Server size
												</RadioGroup.Label>
												<div className="space-y-4">
													{styles.map((sample) => (
														<RadioGroup.Option
															key={sample.id}
															value={sample}
															className={({
																checked,
																active,
															}: {
																checked: boolean;
																active: boolean;
															}) =>
																classNames(
																	checked
																		? "border-transparent"
																		: "border-gray-300",
																	active
																		? "border-blue-500 ring-2 ring-blue-200"
																		: "",
																	"relative cursor-pointer rounded-lg border bg-white w-[400px]   px-6 py-4 shadow-sm focus:outline-none flex justify-between"
																)
															}
														>
															{({
																active,
																checked,
															}: {
																active: boolean;
																checked: boolean;
															}) => (
																<>
																	<span className="flex items-center">
																		<span className="flex flex-col text-sm">
																			<RadioGroup.Label
																				as="span"
																				className="font-medium text-gray-900"
																			>
																				{sample.name}
																			</RadioGroup.Label>
																			<RadioGroup.Description
																				as="span"
																				className="text-gray-500"
																			>
																				<span className="block">
																					{
																						sample.description
																					}
																				</span>
																			</RadioGroup.Description>
																		</span>
																	</span>
																	<RadioGroup.Description
																		as="span"
																		className="flex text-sm ml-4 mt-0 flex-col text-right items-center justify-center"
																	></RadioGroup.Description>
																	<span
																		className={classNames(
																			active
																				? "border"
																				: "border-2",
																			checked
																				? "border-blue-500"
																				: "border-transparent",
																			"pointer-events-none absolute -inset-px rounded-lg"
																		)}
																		aria-hidden="true"
																	/>
																</>
															)}
														</RadioGroup.Option>
													))}
												</div>
											</RadioGroup>
										</div>
										<div className="flex gap-[15px] justify-end mt-8">
											<div>
												<button
													onClick={() => setStep(step - 1)}
													className="group rounded-full px-4 py-2 text-[13px] font-semibold transition-all flex items-center justify-center bg-[#f5f7f9] text-[#1E2B3A] no-underline active:scale-95 scale-100 duration-75"
													style={{
														boxShadow:
															"0 1px 1px #0c192714, 0 1px 3px #0c192724",
													}}
												>
													Previous step
												</button>
											</div>
											<div>
												<button
													onClick={() => {
														setStep(step + 1);
													}}
													className="group rounded-full px-4 py-2 text-[13px] font-semibold transition-all flex items-center justify-center bg-[#1E2B3A] text-white hover:[linear-gradient(0deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.1)), #0D2247] no-underline flex gap-x-2  active:scale-95 scale-100 duration-75"
													style={{
														boxShadow:
															"0px 1px 4px rgba(13, 34, 71, 0.17), inset 0px 0px 0px 1px #061530, inset 0px 0px 0px 2px rgba(255, 255, 255, 0.1)",
													}}
												>
													<span> Continue </span>
													<svg
														className="w-5 h-5"
														viewBox="0 0 24 24"
														fill="none"
														xmlns="http://www.w3.org/2000/svg"
													>
														<path
															d="M13.75 6.75L19.25 12L13.75 17.25"
															stroke="#FFF"
															strokeWidth="1.5"
															strokeLinecap="round"
															strokeLinejoin="round"
														/>
														<path
															d="M19 12H4.75"
															stroke="#FFF"
															strokeWidth="1.5"
															strokeLinecap="round"
															strokeLinejoin="round"
														/>
													</svg>
												</button>
											</div>
										</div>
									</motion.div>
								) : step === 5 ? (
									<motion.div
										initial={{ opacity: 0, y: 40 }}
										animate={{ opacity: 1, y: 0 }}
										exit={{ opacity: 0, y: -40 }}
										key="step-2"
										transition={{
											duration: 0.95,
											ease: [0.165, 0.84, 0.44, 1],
										}}
										className="max-w-lg mx-auto px-4 lg:px-0"
									>
										<div>
											<RadioGroup
												value={selectedMusic}
												onChange={setSelectedMusic}
											>
												<div className="space-y-4">
													{music.map((script) => (
														<RadioGroup.Option
															key={script.name}
															value={script}
															className={({ checked, active }) =>
																classNames(
																	checked
																		? "border-transparent"
																		: "border-gray-300",
																	active
																		? "border-blue-500 ring-2 ring-blue-200"
																		: "",
																	"relative cursor-pointer rounded-lg border bg-white w-[400px]   px-6 py-4 shadow-sm focus:outline-none flex justify-between"
																)
															}
														>
															{({ active, checked }) => (
																<>
																	<span className="flex items-center">
																		<span className="flex flex-col text-sm">
																			<RadioGroup.Label
																				as="span"
																				className="font-medium text-gray-900"
																			>
																				{script.name}
																			</RadioGroup.Label>
																			<RadioGroup.Description
																				as="span"
																				className="text-gray-500"
																			>
																			
																			</RadioGroup.Description>
																		</span>
																		
																	</span>
																	<RadioGroup.Description
																					as="span"
																					className="flex text-sm ml-4 mt-0 flex-col text-right items-center justify-center"
																				>
																					<span className="text-gray-500">
																						<button
																							onClick={() => {
																								if (
																									currentAudio
																								) {
																									currentAudio.pause();
																									currentAudio.currentTime = 0;
																								}
																								const audio =
																									new Audio(
																										script.sampleAudio
																									);
																								audio.play();
																								setCurrentAudio(
																									audio
																								);
																							}}
																							className="group rounded-full px-3 py-1 text-[12px] font-semibold transition-all flex  justify-right bg-[#1E2B3A] text-white hover:bg-[#0D2247] no-underline active:scale-95 scale-100 duration-75"
																							style={{
																								boxShadow:
																									"0px 1px 4px rgba(13, 34, 71, 0.17), inset 0px 0px 0px 1px #061530, inset 0px 0px 0px 2px rgba(255, 255, 255, 0.1)",
																							}}
																						>
																							Play Sample
																						</button>
																					</span>
																				</RadioGroup.Description>
																	<span
																		className={classNames(
																			active
																				? "border"
																				: "border-2",
																			checked
																				? "border-blue-500"
																				: "border-transparent",
																			"pointer-events-none absolute -inset-px rounded-lg"
																		)}
																		aria-hidden="true"
																	/>
																</>
															)}
														</RadioGroup.Option>
													))}
												</div>
											</RadioGroup>
										</div>
										<div className="flex gap-[15px] justify-end mt-8">
											<div>
												<button
													onClick={() => setStep(step - 1)}
													className="group rounded-full px-4 py-2 text-[13px] font-semibold transition-all flex items-center justify-center bg-[#f5f7f9] text-[#1E2B3A] no-underline active:scale-95 scale-100 duration-75"
													style={{
														boxShadow:
															"0 1px 1px #0c192714, 0 1px 3px #0c192724",
													}}
												>
													Previous step
												</button>
											</div>
											<div>
												<button
													onClick={() => {
														setStep(step + 1);
													}}
													className="group rounded-full px-4 py-2 text-[13px] font-semibold transition-all flex items-center justify-center bg-[#1E2B3A] text-white hover:[linear-gradient(0deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.1)), #0D2247] no-underline flex gap-x-2  active:scale-95 scale-100 duration-75"
													style={{
														boxShadow:
															"0px 1px 4px rgba(13, 34, 71, 0.17), inset 0px 0px 0px 1px #061530, inset 0px 0px 0px 2px rgba(255, 255, 255, 0.1)",
													}}
												>
													<span> Continue </span>
													<svg
														className="w-5 h-5"
														viewBox="0 0 24 24"
														fill="none"
														xmlns="http://www.w3.org/2000/svg"
													>
														<path
															d="M13.75 6.75L19.25 12L13.75 17.25"
															stroke="#FFF"
															strokeWidth="1.5"
															strokeLinecap="round"
															strokeLinejoin="round"
														/>
														<path
															d="M19 12H4.75"
															stroke="#FFF"
															strokeWidth="1.5"
															strokeLinecap="round"
															strokeLinejoin="round"
														/>
													</svg>
												</button>
											</div>
										</div>
									</motion.div>
								) : step === 6 ? (
									<motion.div
										initial={{ opacity: 0, y: 40 }}
										animate={{ opacity: 1, y: 0 }}
										exit={{ opacity: 0, y: -40 }}
										key="step-2"
										transition={{
											duration: 0.95,
											ease: [0.165, 0.84, 0.44, 1],
										}}
										className="max-w-lg mx-auto px-4 lg:px-0"
									>
										<div>
											<div className="space-y-4">
												{Object.entries(topics).length > 0 ? (
													Object.entries(topics).map(
														([key, value], index) => (
															<CustomCheckbox
																key={index}
																checked={selectedTopics.includes(
																	key
																)}
																onChange={() => {
																	const topic = key;
																	setSelectedTopics(
																		(prevSelectedTopics) => {
																			if (
																				prevSelectedTopics.includes(
																					topic
																				)
																			) {
																				return prevSelectedTopics.filter(
																					(t) =>
																						t !== topic
																				);
																			} else {
																				return [
																					...prevSelectedTopics,
																					topic,
																				];
																			}
																		}
																	);
																}}
																label={key}
															/>
														)
													)
												) : (
													<p>Loading data...</p>
												)}
											</div>

											<ul>
												{serverIds.map((item, index) => (
													<li key={index}>
														{JSON.parse(item).topicextraction}
													</li>
												))}
											</ul>

											<div className="flex gap-[15px] justify-end mt-8">
												<div>
													<button
														onClick={() => setStep(step - 1)}
														className="group rounded-full px-4 py-2 text-[13px] font-semibold transition-all flex items-center justify-center bg-[#f5f7f9] text-[#1E2B3A] no-underline active:scale-95 scale-100 duration-75"
														style={{
															boxShadow:
																"0 1px 1px #0c192714, 0 1px 3px #0c192724",
														}}
													>
														Previous step
													</button>
												</div>
												<div>
													<button
														onClick={() => {
															setStep(step + 1);
														}}
														className="group rounded-full px-4 py-2 text-[13px] font-semibold transition-all flex items-center justify-center bg-[#1E2B3A] text-white hover:[linear-gradient(0deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.1)), #0D2247] no-underline flex gap-x-2  active:scale-95 scale-100 duration-75"
														style={{
															boxShadow:
																"0px 1px 4px rgba(13, 34, 71, 0.17), inset 0px 0px 0px 1px #061530, inset 0px 0px 0px 2px rgba(255, 255, 255, 0.1)",
														}}
													>
														<span> Continue </span>
														<svg
															className="w-5 h-5"
															viewBox="0 0 24 24"
															fill="none"
															xmlns="http://www.w3.org/2000/svg"
														>
															<path
																d="M13.75 6.75L19.25 12L13.75 17.25"
																stroke="#FFF"
																strokeWidth="1.5"
																strokeLinecap="round"
																strokeLinejoin="round"
															/>
															<path
																d="M19 12H4.75"
																stroke="#FFF"
																strokeWidth="1.5"
																strokeLinecap="round"
																strokeLinejoin="round"
															/>
														</svg>
													</button>
												</div>
											</div>
										</div>
									</motion.div>
								) : step === 7 ? (
									<motion.div
										initial={{ opacity: 0, y: 40 }}
										animate={{ opacity: 1, y: 0 }}
										exit={{ opacity: 0, y: -40 }}
										key="step-2"
										transition={{
											duration: 0.95,
											ease: [0.165, 0.84, 0.44, 1],
										}}
										className="max-w-xl  object-left-top	 lg:px-0"
									>
										{loadingScript ? (
											<p>Loading...</p>
										) : (
											<>
												<textarea
													value={scriptValue}
													onChange={(e) =>
														setScriptValue(e.target.value)
													}
													className="border border-gray-300 rounded-md p-2 w-[600px] h-[400px] focus:outline-none focus:ring-2 focus:ring-[#1E2B3A] focus:border-transparent transition-all duration-150 ease-in-out resize-none"
													placeholder="Enter your script..."
												></textarea>
											</>
										)}

										<div className="flex gap-[15px] justify-end mt-8">
											<div>
												<button
													onClick={() => setStep(step - 1)}
													className="group rounded-full px-4 py-2 text-[13px] font-semibold transition-all flex items-center justify-center bg-[#f5f7f9] text-[#1E2B3A] no-underline active:scale-95 scale-100 duration-75"
													style={{
														boxShadow:
															"0 1px 1px #0c192714, 0 1px 3px #0c192724",
													}}
												>
													Previous step
												</button>
											</div>
											<div>
												<button
													onClick={() => {
														setScriptRefresh(scriptRefresh + 1);
													}}
													className="group rounded-full px-4 py-2 text-[13px] font-semibold transition-all flex items-center justify-center bg-blue-800 text-white no-underline active:scale-95 scale-100 duration-75"
													style={{
														boxShadow:
															"0 1px 1px #0c192714, 0 1px 3px #0c192724",
													}}
												>
													Regenerate
												</button>
											</div>

											<div>
												<button
													onClick={() => {
														setStep(step + 1);
													}}
													className="group rounded-full px-4 py-2 text-[13px] font-semibold transition-all flex items-center justify-center bg-[#1E2B3A] text-white hover:[linear-gradient(0deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.1)), #0D2247] no-underline flex gap-x-2  active:scale-95 scale-100 duration-75"
													style={{
														boxShadow:
															"0px 1px 4px rgba(13, 34, 71, 0.17), inset 0px 0px 0px 1px #061530, inset 0px 0px 0px 2px rgba(255, 255, 255, 0.1)",
													}}
												>
													<span> Continue </span>
													<svg
														className="w-5 h-5"
														viewBox="0 0 24 24"
														fill="none"
														xmlns="http://www.w3.org/2000/svg"
													>
														<path
															d="M13.75 6.75L19.25 12L13.75 17.25"
															stroke="#FFF"
															strokeWidth="1.5"
															strokeLinecap="round"
															strokeLinejoin="round"
														/>
														<path
															d="M19 12H4.75"
															stroke="#FFF"
															strokeWidth="1.5"
															strokeLinecap="round"
															strokeLinejoin="round"
														/>
													</svg>
												</button>
											</div>
										</div>
									</motion.div>
								) : step === 8 ? (
									<motion.div
										initial={{ opacity: 0, y: 40 }}
										animate={{ opacity: 1, y: 0 }}
										exit={{ opacity: 0, y: -40 }}
										key="step-2"
										transition={{
											duration: 0.95,
											ease: [0.165, 0.84, 0.44, 1],
										}}
										className="max-w-xl  object-left-top	 lg:px-0"
									>
										{videoError ? (
											<p>
												Error loading the video. Please try again.
											</p>
										) : videoLoading ? (
											<h1>
												<Typewriter
													options={{
														strings: [
															'<p class="text-2xl text-violet-800	"> Summoning pixels from the digital realm... </p>',
															'<p class="text-2xl text-teal-800"	> Coaxing frames out of hiding... </p>',
															'<p class="text-2xl text-emerald-800"	> Sprinkling virtual fairy dust on your video... </p>',
															'<p class="text-2xl text-amber-800"	> Convincing the video elves to work their magic... </p>',
															'<p class="text-2xl text-red-800"	> Brewing up a fresh batch of moving pictures... </p>',
														],
														autoStart: true,
														loop: true,
														delay: 50,
													}}
												/>
											</h1>
										) : (
											<ReactPlayer controls={true} url={videoUrl} />
										)}
										<ul>
											{serverIds.map((item, index) => (
												<li key={index}>
													{JSON.parse(item).texttospeech}
												</li>
											))}
										</ul>

										<div className="flex gap-[15px] justify-end mt-8">
											<div>
												<button
													onClick={() => setStep(step - 1)}
													className="group rounded-full px-4 py-2 text-[13px] font-semibold transition-all flex items-center justify-center bg-[#f5f7f9] text-[#1E2B3A] no-underline active:scale-95 scale-100 duration-75"
													style={{
														boxShadow:
															"0 1px 1px #0c192714, 0 1px 3px #0c192724",
													}}
												>
													Previous step
												</button>
											</div>
											<div>
												<button
													onClick={() => {
														setStep(1);
													}}
													className="group rounded-full px-4 py-2 text-[13px] font-semibold transition-all flex items-center justify-center bg-[#1E2B3A] text-white hover:[linear-gradient(0deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.1)), #0D2247] no-underline flex gap-x-2  active:scale-95 scale-100 duration-75"
													style={{
														boxShadow:
															"0px 1px 4px rgba(13, 34, 71, 0.17), inset 0px 0px 0px 1px #061530, inset 0px 0px 0px 2px rgba(255, 255, 255, 0.1)",
													}}
												>
													<span> Start again </span>
													<svg
														className="w-5 h-5"
														viewBox="0 0 24 24"
														fill="none"
														xmlns="http://www.w3.org/2000/svg"
													>
														<path
															d="M13.75 6.75L19.25 12L13.75 17.25"
															stroke="#FFF"
															strokeWidth="1.5"
															strokeLinecap="round"
															strokeLinejoin="round"
														/>
														<path
															d="M19 12H4.75"
															stroke="#FFF"
															strokeWidth="1.5"
															strokeLinecap="round"
															strokeLinejoin="round"
														/>
													</svg>
												</button>
											</div>
										</div>
									</motion.div>
								) : (
									<div></div>
								)}
							</div>
						</div>
						<div className="h-full w-full bg-[#F1F2F4] relative flex justify-center items-center">
							<figure
								className="inline-block align-middle sm:scale-[0.6] md:scale-[130%] w-2/3 h-1/2 bg-[#f5f7f9] text-[9px] origin-[50%_15%] md:origin-[50%_25%] rounded-[15px] overflow-hidden p-2 z-20"
								style={{
									grid: "100%/repeat(1,calc(5px * 28)) 1fr",
									boxShadow:
										"0 192px 136px rgba(26,43,59,.23),0 70px 50px rgba(26,43,59,.16),0 34px 24px rgba(26,43,59,.13),0 17px 12px rgba(26,43,59,.1),0 7px 5px rgba(26,43,59,.07), 0 50px 100px -20px rgb(50 50 93 / 25%), 0 30px 60px -30px rgb(0 0 0 / 30%), inset 0 -2px 6px 0 rgb(10 37 64 / 35%)",
								}}
							>
								<div className="overflow-auto">
									{" "}
									<ul>
										{" "}
										{step < 2 && (
											<>
												{" "}
												{serverIds.map((item, index) => (
													<li key={index}>
														{JSON.parse(item).parsedText}
													</li>
												))}{" "}
											</>
										)}
									</ul>{" "}
									<ul>
										{step >= 2 && step < 8 && (
											<div className="p-4">
												<p className="text-lg font-bold mb-2">
													Selected Options:
												</p>
												<ul className="text-base">
													{step >= 3 && (
														<li>
															<strong>Length:</strong>{" "}
															{selectedLength.name}
														</li>
													)}
													{step >= 4 && (
														<li>
															<strong>Voice:</strong>{" "}
															{selectedVoice.name}
														</li>
													)}
													{step >= 5 && (
														<li>
															<strong>Style:</strong>{" "}
															{selectedStyle.name}
														</li>
													)}
													{step >= 6 && (
														<li>
															<strong>Music:</strong>{" "}
															{selectedMusic.name}
														</li>
													)}
													{step >= 7 && (
														<li>
															<strong>Topic:</strong>{" "}
															{selectedTopics.join(", ")}{" "}
														</li>
													)}
												</ul>
											</div>
										)}{" "}
										{step === 7 && (
											<>
												{" "}
												{lastScriptValues.map((value, index) => (
													<li key={index} className="p-2">
														{" "}
														<button
															onClick={() =>
																setScriptValue(
																	lastScriptValues[index]
																)
															}
															className="group rounded-full px-4 py-2 text-[13px] font-semibold transition-all flex items-center justify-center bg-emerald-800 text-white no-underline active:scale-95 scale-100 duration-75 p-4"
															style={{
																boxShadow:
																	"0 1px 1px #0c192714, 0 1px 3px #0c192724",
															}}
														>
															Version {index + 1}
														</button>
													</li>
												))}
											</>
										)}{" "}
									</ul>{" "}
								</div>
							</figure>
						</div>
					</div>
				)}
			</AnimatePresence>
		</div>
	);
}