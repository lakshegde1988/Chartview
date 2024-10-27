import fs from 'fs';
import path from 'path';
import Papa from 'papaparse';

export default function handler(req, res) {
  const filePath = path.join(process.cwd(), 'public', 'stocks.csv');
  const file = fs.readFileSync(filePath, 'utf8');

  // Parse CSV data
  const { data } = Papa.parse(file, { header: true });
  
  res.status(200).json(data);
}
