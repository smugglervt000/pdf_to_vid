import React from 'react';

interface StepIndicatorProps {
    currentStep: number; // Specify that currentStep should be a number
  }
  
  const StepIndicator: React.FC<StepIndicatorProps> = ({ currentStep }) => {
    const getStepColorClass = (stepNumber: number) => {
    if (stepNumber < currentStep) {
      return 'bg-green-200 text-green-500 dark:bg-green-900 dark:text-green-400'; // Completed Step
    } else if (stepNumber === currentStep) {
      return 'bg-blue-200 text-blue-500 dark:bg-blue-900 dark:text-blue-400'; // Current Step
    } else {
      return 'bg-gray-100 text-gray-500 dark:bg-gray-700 dark:text-gray-400'; // Future Step
    }
  };

  return (
    <ol className="relative text-gray-700 border-s border-gray-200 dark:border-gray-700 dark:text-gray-400">
      {Array.from({ length: 8 }, (_, i) => (
        <li key={i} className="mb-10 ms-6">
          <span
            className={`absolute flex items-center justify-center w-8 h-10 rounded-full -start-4 ring-4 ring-white dark:ring-gray-900 ${getStepColorClass(i + 1)}`}
          >
            {/* SVG icons could be extracted to a separate component if they are not unique */}
            {/* ... SVG content */}
          </span>
          <h3 className="font-medium leading-tight"> Step {i + 1}</h3>
            <p className="mt-2 textlg text-gray-500 dark:text-gray-400">
                {/* Step description */}
                {/* if step 1 */}
                {i === 0 && 'Upload your file'}
                {/* if step 2 */}
                {i === 1 && 'Select video length'}
                {/* if step 3 */}
                {i === 2 && 'Select your voiceover speaker'}

                {i === 3 && 'Select style'}

                {/* if step 4 */}
                {i === 4 && 'Choose your background music'}

                {i === 5 && 'Choose your topics'}
                {/* if step 5 */}
                {/* if step 6 */}

                {i === 6 && 'Edit your script'}

                {/* if step 7 */}
                {i === 7 && 'Video generation'}
                {/* if step 8 */}


            </p>

        </li>
      ))}
    </ol>
  );
};

export default StepIndicator;