import { AgentState } from "@/lib/types";

export interface PrescriptionsCardProps {
  state: AgentState;
  setState: (state: AgentState) => void;
}

export function PrescriptionsCard({ state, setState }: PrescriptionsCardProps) {
  return (
    <div className="bg-white/20 backdrop-blur-md p-8 rounded-2xl shadow-xl max-w-2xl w-full">
      <h1 className="text-4xl font-bold text-white mb-2 text-center">Prescriptions</h1>
      <p className="text-gray-200 text-center italic mb-6">Manage your medications and dosages here. 💊</p>
      <hr className="border-white/20 my-6" />
      <div className="flex flex-col gap-3">
        {state.prescriptions?.map((prescription, index) => (
          <div 
            key={index} 
            className="bg-white/15 p-4 rounded-xl text-white relative group hover:bg-white/20 transition-all"
          >
            <p className="pr-8">{prescription}</p>
            <button 
              onClick={() => setState({
                ...state,
                prescriptions: state.prescriptions?.filter((_, i) => i !== index),
              })}
              className="absolute right-3 top-3 opacity-0 group-hover:opacity-100 transition-opacity 
                bg-red-500 hover:bg-red-600 text-white rounded-full h-6 w-6 flex items-center justify-center"
            >
              ✕
            </button>
          </div>
        ))}
      </div>
      {state.prescriptions?.length === 0 && <p className="text-center text-white/80 italic my-8">
        No prescriptions yet. Ask the assistant to add some!
      </p>}
    </div>
  );
}