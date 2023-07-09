// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const response = await fetch(`http://back-api:8000/start/monitor?url=${req.query.url}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json()
    res.status(200).json(data)
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Unexpected error", info: error })
  }

}
