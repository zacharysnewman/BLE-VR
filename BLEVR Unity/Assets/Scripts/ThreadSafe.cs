using System;
using System.Collections.Generic;
using System.Collections.Concurrent;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace SoloLearn
{
    class Program
    {
        static void Main(string[] args)
        {

        }

        public bool ShouldRun = true;
        private readonly AutoResetEvent _signal = new AutoResetEvent(false);
        private readonly ConcurrentQueue<string> _queue = new ConcurrentQueue<string>();

        void ProducerThread()
        {
            while (ShouldRun)
            {
                string item = GetNextItem();
                _queue.Enqueue(item);
                _signal.Set();
            }
        }

        void ConsumerThread()
        {
            while (ShouldRun)
            {
                _signal.WaitOne();

                string item = null;
                while (_queue.TryDequeue(out item))
                {
                    // Use Data From Socket
                }
            }
        }

        string GetNextItem()
        {
            // Get Data From Socket
            return "";
        }

    }
}
