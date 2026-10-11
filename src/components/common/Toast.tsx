import React from 'react';
import { CheckCircle2, Info, AlertTriangle, X } from 'lucide-react';
import { useApp } from '../../context/AppContext';

export const Toast: React.FC = () => {
  const { toast } = useApp();

  if (!toast) return null;

  const icons = {
    success: <CheckCircle2 className="w-4 h-4 text-[#36C98F]" />,
    info: <Info className="w-4 h-4 text-[#8B7CFF]" />,
    warning: <AlertTriangle className="w-4 h-4 text-[#F5B942]" />,
  };

  const borderColor = {
    success: 'border-[#36C98F]/30',
    info: 'border-[#8B7CFF]/30',
    warning: 'border-[#F5B942]/30',
  };

  const bgGlow = {
    success: 'shadow-[0_0_30px_-8px_rgba(54,201,143,0.15)]',
    info: 'shadow-[0_0_30px_-8px_rgba(139,124,255,0.15)]',
    warning: 'shadow-[0_0_30px_-8px_rgba(245,185,66,0.15)]',
  };

  return (
    <div className={`fixed bottom-6 right-6 z-[9999] animate-fade-in-up`}>
      <div className={`glass flex items-center gap-3 px-5 py-3.5 rounded-2xl ${borderColor[toast.type]} ${bgGlow[toast.type]} max-w-sm`}>
        <div className="flex-shrink-0">{icons[toast.type]}</div>
        <p className="text-xs font-medium text-[#F5F5F5] leading-relaxed">{toast.message}</p>
      </div>
    </div>
  );
};
