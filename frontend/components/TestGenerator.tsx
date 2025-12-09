import React, { useState } from 'react';
import axios from 'axios';

const TestGenerator = () => {
    const [requirements, setRequirements] = useState('');
    const [testType, setTestType] = useState('UI');
    const [generatedCode, setGeneratedCode] = useState('');

    const generateTests = async () => {
        try {
            const response = await axios.post('/api/generate', {
                requirements,
                type: testType
            });
            setGeneratedCode(response.data.code);
        } catch (error) {
            console.error('Error generating tests:', error);
        }
    };

    return (
        <div>
            <textarea value={requirements} onChange={(e) => setRequirements(e.target.value)} />
            <select value={testType} onChange={(e) => setTestType(e.target.value)}>
                <option value="UI">UI</option>
                <option value="API">API</option>
            </select>
            <button onClick={generateTests}>Generate</button>
            <pre>{generatedCode}</pre>
        </div>
    );
};