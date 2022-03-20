// Version number as a tuple.
(int, int, int) version = (0, 0, 0);

string versionString = String.Format("{0}.{1}.{2}", version.Item1, version.Item2, version.Item3);

Console.WriteLine("I'll do something soon!\n");

Console.WriteLine($"nowPlaying version {versionString}");